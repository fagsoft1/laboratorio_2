import os
from smtplib import SMTPException

from django.core.mail import EmailMultiAlternatives
from django.db.models import Q, Count, F
from io import BytesIO

from django.template.loader import get_template, render_to_string
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework import viewsets, serializers
from weasyprint import HTML, CSS

from ordenes.mixins import OrdenesResultadosMixin
from .api_serializers import OrdenSerializer, OrdenExamenSerializer
from .models import Orden, OrdenExamen, OrdenExamenFirmas
from medicos.models import Especialista


# from examenes_especiales.models import Biopsia, Citologia

def get_page_body(boxes):
    for box in boxes:
        if box.element_tag == 'body':
            return box
        return get_page_body(box.all_children())


class OrdenViewSet(OrdenesResultadosMixin, viewsets.ModelViewSet):
    queryset = Orden.objects.select_related(
        'medico_remitente',
        'paciente',
        'entidad',
        'elaborado_por'
    ).prefetch_related(
        'mis_examenes__examen',
        'mis_examenes__mis_firmas',
        'mis_examenes__mis_firmas__especialista',
        'mis_examenes__mis_firmas__especialista__especialidad',
        'mis_examenes__examen__subgrupo_cups',
    ).all()
    serializer_class = OrdenSerializer

    @detail_route(methods=['post'])
    def enviar_email(self, request, pk=None):
        orden = self.get_object()
        context_examenes = {}

        tipo_envio = request.POST.get('tipo_envio')

        send_to = []

        if tipo_envio == 'Cliente' or tipo_envio == 'Ambos':
            send_to.append(orden.paciente.email)

        if tipo_envio == 'Entidad' or tipo_envio == 'Ambos':
            send_to.extend([x.correo_electronico for x in orden.entidad.mis_contactos.filter(enviar_correo=True)])

        self.generar_resultados(orden, context_examenes)

        text_content = render_to_string('email/ordenes/resultados/cuerpo_correo.html', {})

        ctx = {
            'una_firma': context_examenes['una_firma'],
            'multifirma': context_examenes['multifirma'],
            'paciente': orden.paciente,
            'orden': orden,
            'entidad': orden.entidad,
            'medico_remitente': orden.medico_remitente,
        }

        # https://gist.github.com/pikhovkin/5642563

        html_get_template = get_template('email/ordenes/resultados/resultados.html').render(ctx)

        html = HTML(
            string=html_get_template,
            base_url=request.build_absolute_uri()
        )

        main_doc = html.render()

        ctx = {
            'titulo': 'titulo de prueba ctx',
        }
        html_get_template = get_template('email/cabecera.html').render(ctx)
        html = HTML(
            string=html_get_template,
            base_url=request.build_absolute_uri()
        )
        header = html.render(
            stylesheets=[CSS(string='div {position: fixed; top: 1cm; left: 1cm;}')])

        header_page = header.pages[0]
        header_body = get_page_body(header_page._page_box.all_children())
        header_body = header_body.copy_with_children(header_body.all_children())

        html_get_template = get_template('email/pie_pagina.html').render(ctx)
        html = HTML(
            string=html_get_template,
            base_url=request.build_absolute_uri()
        )
        footer = html.render(
            stylesheets=[CSS(string='div {position: fixed; bottom: 1cm; left: 1cm;}')])

        footer_page = footer.pages[0]
        footer_body = get_page_body(footer_page._page_box.all_children())
        footer_body = footer_body.copy_with_children(header_body.all_children())

        for i, page in enumerate(main_doc.pages):
            page_body = get_page_body(page._page_box.all_children())

            page_body.children += header_body.all_children()
            page_body.children += footer_body.all_children()

        output = BytesIO()
        main_doc.write_pdf(
            target=output
        )

        # main_doc.write_pdf(
        #     target='correo-prueba.pdf'
        # )

        msg = EmailMultiAlternatives(
            'Resultados de examenes',
            text_content,
            'Laboratorios Collazos <webmaster@odecopack.co>',
            to=send_to
        )
        msg.attach_alternative(text_content, "text/html")
        msg.attach('Resultados Orden de Laboratorio %s' % orden.id, output.getvalue(), 'application/pdf')
        try:
            msg.send()
        except Exception as e:
            raise serializers.ValidationError('Se há presentado un error al intentar enviar el correo, envío fallido')
        return Response({'resultado': 'ok'})

    @list_route(methods=['get'])
    def buscar_x_parametro(self, request):
        parametro = request.GET.get('parametro')
        qs = None
        if len(parametro) > 0:
            qs = self.get_queryset().filter(
                Q(paciente__nombre__icontains=parametro) |
                Q(paciente__nombre_segundo__icontains=parametro) |
                Q(paciente__apellido__icontains=parametro) |
                Q(paciente__apellido_segundo__icontains=parametro) |
                Q(paciente__nro_identificacion__icontains=parametro) |
                Q(id__icontains=parametro)
            ).distinct().order_by('-pk')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(elaborado_por=self.request.user)


class OrdenExamenViewSet(viewsets.ModelViewSet):
    queryset = OrdenExamen.objects.select_related(
        'orden',
        'orden__paciente',
        'examen__subgrupo_cups',
        'orden__entidad',
        # 'mi_biopsia',
        # 'mi_citologia'
    ).prefetch_related(
        # 'mis_bitacoras__generado_por',
        'mis_firmas__especialista',
        'mis_firmas__especialista__especialidad'
    ).all().order_by('pk')
    serializer_class = OrdenExamenSerializer

    @list_route(methods=['get'])
    def pendientes(self, request):
        qs = self.get_queryset().filter(orden__estado=1, examen_estado=0)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def con_resultados(self, request):
        qs = self.get_queryset().filter(orden__estado=1, examen_estado=1)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def verificados(self, request):
        qs = self.get_queryset().filter(orden__estado=1, examen_estado__in=[2, 3])
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def firmar(self, request, pk=None):
        orden_examen = self.get_object()
        id_especialista = self.request.POST.get('id_especialista')
        especialista = None
        if not id_especialista:
            user = self.request.user
            if hasattr(user, 'especialista'):
                if hasattr(user.especialista, 'firma'):
                    especialista = user.especialista
        else:
            especialista = Especialista.objects.get(id=id_especialista)
        if especialista:
            orden_examen.firmar(especialista)
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    @detail_route(methods=['post', 'get'])
    def quitar_firma(self, request, pk=None):
        id_firma = int(request.POST.get('id_firma'))
        orden_examen = self.get_object()
        firma = orden_examen.mis_firmas.filter(id=id_firma).all()
        firma.delete()
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    def perform_create(self, serializer):
        orden_examen = serializer.save(creado_por=self.request.user)

    #     if orden_examen.especial:
    #         if orden_examen.nro_plantilla == 1:
    #             Biopsia.objects.create(orden_examen=orden_examen)
    #         if orden_examen.nro_plantilla == 2:
    #             Citologia.objects.create(orden_examen=orden_examen)

    def perform_update(self, serializer):
        serializer.save(modificado_por=self.request.user)

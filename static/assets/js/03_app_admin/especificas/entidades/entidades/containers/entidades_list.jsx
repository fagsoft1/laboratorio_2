import React, {Component, Fragment} from 'react';
import {connect} from "react-redux";
import * as actions from "../../../../../01_actions/01_index";
import CargarDatos from "../../../../../00_utilities/components/system/cargar_datos";
import {Titulo} from "../../../../../00_utilities/templates/fragmentos";
import BloqueEntidades from '../components/entidades_bloque';
import ValidarPermisos from "../../../../../00_utilities/permisos/validar_permisos";
import {permisosAdapter} from "../../../../../00_utilities/common";
import {ENTIDADES as entidades_permisos} from "../../../../../00_utilities/permisos/types";

class ListadoElementos extends Component {
    constructor(props) {
        super(props);
        this.state = {
            slideIndex: 0,
        };
        this.elemento_plural = 'Entidades';
        this.elemento_singular = 'Entidad';
        this.cargarDatos = this.cargarDatos.bind(this);
        this.error_callback = this.error_callback.bind(this);

    }

    componentDidMount() {
        this.cargarDatos();
    }

    error_callback(error) {
        this.props.notificarErrorAjaxAction(error);
    }


    componentWillUnmount() {
        this.props.clearEntidades();
    }

    cargarDatos() {
        this.props.cargando();
        const cargarEntidades = () => this.props.fetchEntidades(() => this.props.noCargando(), this.error_callback);
        this.props.fetchMisPermisos(cargarEntidades, this.error_callback)
    }

    render() {
        const {entidades_list, mis_permisos} = this.props;
        const permisos = permisosAdapter(mis_permisos, entidades_permisos);
        return (
            <ValidarPermisos can_see={permisos.list} nombre='Entidades'>
                <Titulo>{`Entidades`}</Titulo>
                <BloqueEntidades {...this.props} list={entidades_list} mis_permisos={mis_permisos}/>
                <CargarDatos
                    cargarDatos={this.cargarDatos}
                />
            </ValidarPermisos>
        )
    }
}

function mapPropsToState(state, ownProps) {
    return {
        mis_permisos: state.mis_permisos,
        entidades_list: state.entidades

    }
}

export default connect(mapPropsToState, actions)(ListadoElementos)
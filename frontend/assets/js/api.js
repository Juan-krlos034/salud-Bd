// =====================================================
// API.JS - Módulo de conexión con Backend Django
// Guardar en: assets/js/api.js
// =====================================================

const API_BASE_URL = 'http://localhost:8000/api';

// =====================================================
// UTILIDADES
// =====================================================

/**
 * Realiza peticiones HTTP al backend
 */
async function fetchAPI(endpoint, options = {}) {
    const config = {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        },
        ...options
    };

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        
        // Si la respuesta no es ok, lanzar error con el detalle
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Error ${response.status}`);
        }

        // Si es 204 No Content, retornar null
        if (response.status === 204) {
            return null;
        }

        return await response.json();
    } catch (error) {
        console.error('Error en API:', error);
        throw error;
    }
}

/**
 * Obtiene el usuario actual del sessionStorage
 */
function getCurrentUser() {
    const userStr = sessionStorage.getItem('sr_user');
    return userStr ? JSON.parse(userStr) : null;
}

/**
 * Guarda el usuario en sessionStorage
 */
function saveUser(userData) {
    sessionStorage.setItem('sr_user', JSON.stringify(userData));
}

/**
 * Cierra sesión
 */
function logout() {
    sessionStorage.removeItem('sr_user');
    window.location.href = '/login.html';
}

/**
 * Verifica si el usuario está autenticado
 */
function requireAuth() {
    const user = getCurrentUser();
    if (!user) {
        window.location.href = '/login.html';
        return false;
    }
    return true;
}

/**
 * Verifica si el usuario tiene un rol específico
 */
function requireRole(role) {
    const user = getCurrentUser();
    if (!user || user.rol !== role) {
        alert('No tienes permisos para acceder a esta página');
        window.location.href = '/index.html';
        return false;
    }
    return true;
}

// =====================================================
// API DE USUARIOS
// =====================================================

const UsuariosAPI = {
    /**
     * Login de usuario
     */
    async login(correo, contrasena) {
        const data = await fetchAPI('/usuarios/login/', {
            method: 'POST',
            body: JSON.stringify({ correo, contrasena })
        });
        
        // Guardar usuario en sessionStorage
        saveUser(data);
        return data;
    },

    /**
     * Registrar nuevo usuario
     */
    async register(userData) {
        return await fetchAPI('/usuarios/', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    },

    /**
     * Obtener lista de todos los usuarios
     */
    async getAll() {
        return await fetchAPI('/usuarios/');
    },

    /**
     * Obtener un usuario por ID
     */
    async getById(id) {
        return await fetchAPI(`/usuarios/${id}/`);
    },

    /**
     * Actualizar usuario
     */
    async update(id, userData) {
        return await fetchAPI(`/usuarios/${id}/`, {
            method: 'PUT',
            body: JSON.stringify(userData)
        });
    },

    /**
     * Eliminar usuario
     */
    async delete(id) {
        return await fetchAPI(`/usuarios/${id}/`, {
            method: 'DELETE'
        });
    },

    /**
     * Buscar usuarios
     */
    async search(query) {
        return await fetchAPI(`/usuarios/buscar/?q=${encodeURIComponent(query)}`);
    },

    /**
     * Resetear contraseña
     */
    async resetPassword(correo, nuevaContrasena) {
        return await fetchAPI('/usuarios/reset_password/', {
            method: 'POST',
            body: JSON.stringify({ 
                correo, 
                nueva_contrasena: nuevaContrasena 
            })
        });
    }
};

// =====================================================
// API DE MÉDICOS (placeholder - implementar cuando tengas endpoints)
// =====================================================

const MedicosAPI = {
    /**
     * Obtener todos los médicos
     */
    async getAll() {
        // TODO: Implementar cuando tengas el endpoint
        // return await fetchAPI('/medicos/');
        
        // Datos de ejemplo mientras tanto
        return [
            {
                id: 1,
                id_usuario: 1,
                nombre: 'Dra. Ana Pérez',
                apellidos: 'Pérez González',
                especialidad: 'Pediatría',
                foto: '/assets/img/med1.svg',
                rating: 4.8,
                descripcion: 'Pediatra con 10 años de experiencia en zonas rurales.',
                experiencia: '10 años',
                licencia: 'LIC-12345'
            },
            {
                id: 2,
                id_usuario: 2,
                nombre: 'Dr. Juan Gómez',
                apellidos: 'Gómez Martínez',
                especialidad: 'Cardiología',
                foto: '/assets/img/med2.svg',
                rating: 4.6,
                descripcion: 'Cardiólogo especializado en seguimiento preventivo.',
                experiencia: '15 años',
                licencia: 'LIC-67890'
            },
            {
                id: 3,
                id_usuario: 3,
                nombre: 'Dra. Carla Ruiz',
                apellidos: 'Ruiz López',
                especialidad: 'Medicina General',
                foto: '/assets/img/med3.svg',
                rating: 4.7,
                descripcion: 'Enfoque en medicina familiar y preventiva.',
                experiencia: '8 años',
                licencia: 'LIC-11223'
            }
        ];
    },

    /**
     * Obtener médico por ID
     */
    async getById(id) {
        const medicos = await this.getAll();
        return medicos.find(m => m.id === parseInt(id));
    },

    /**
     * Buscar médicos por especialidad o nombre
     */
    async search(query) {
        const medicos = await this.getAll();
        const q = query.toLowerCase();
        return medicos.filter(m => 
            m.nombre.toLowerCase().includes(q) ||
            m.apellidos.toLowerCase().includes(q) ||
            m.especialidad.toLowerCase().includes(q) ||
            m.descripcion.toLowerCase().includes(q)
        );
    }
};

// =====================================================
// API DE CITAS (placeholder - implementar cuando tengas endpoints)
// =====================================================

const CitasAPI = {
    /**
     * Crear nueva cita
     */
    async create(citaData) {
        // TODO: Implementar cuando tengas el endpoint
        // return await fetchAPI('/citas/', {
        //     method: 'POST',
        //     body: JSON.stringify(citaData)
        // });

        // Mientras tanto, guardar en localStorage
        const citas = JSON.parse(localStorage.getItem('sr_citas') || '[]');
        const nuevaCita = {
            id: Date.now(),
            ...citaData,
            estado: 'Programada',
            fecha_creacion: new Date().toISOString()
        };
        citas.push(nuevaCita);
        localStorage.setItem('sr_citas', JSON.stringify(citas));
        return nuevaCita;
    },

    /**
     * Obtener citas de un paciente
     */
    async getByPaciente(pacienteId) {
        // TODO: Implementar cuando tengas el endpoint
        const citas = JSON.parse(localStorage.getItem('sr_citas') || '[]');
        return citas.filter(c => c.id_paciente === pacienteId);
    },

    /**
     * Obtener citas de un médico
     */
    async getByMedico(medicoId) {
        // TODO: Implementar cuando tengas el endpoint
        const citas = JSON.parse(localStorage.getItem('sr_citas') || '[]');
        return citas.filter(c => c.id_medico === medicoId);
    },

    /**
     * Cancelar cita
     */
    async cancel(citaId) {
        // TODO: Implementar cuando tengas el endpoint
        const citas = JSON.parse(localStorage.getItem('sr_citas') || '[]');
        const index = citas.findIndex(c => c.id === citaId);
        if (index !== -1) {
            citas[index].estado = 'Cancelada';
            localStorage.setItem('sr_citas', JSON.stringify(citas));
            return citas[index];
        }
        throw new Error('Cita no encontrada');
    },

    /**
     * Obtener todas las citas
     */
    async getAll() {
        const citas = JSON.parse(localStorage.getItem('sr_citas') || '[]');
        return citas;
    }
};

// =====================================================
// API DE AGENDA (placeholder)
// =====================================================

const AgendaAPI = {
    /**
     * Obtener disponibilidad de un médico
     */
    async getDisponibilidad(medicoId) {
        // TODO: Implementar cuando tengas el endpoint
        // Retornar horarios de ejemplo
        return [
            { fecha: '2025-10-17', hora: '09:00', disponible: true },
            { fecha: '2025-10-17', hora: '10:00', disponible: true },
            { fecha: '2025-10-17', hora: '11:00', disponible: false },
            { fecha: '2025-10-17', hora: '14:00', disponible: true },
            { fecha: '2025-10-18', hora: '09:00', disponible: true },
            { fecha: '2025-10-18', hora: '15:00', disponible: true }
        ];
    }
};

// =====================================================
// API DE HISTORIA CLÍNICA (placeholder)
// =====================================================

const HistoriaAPI = {
    /**
     * Obtener historia clínica de un paciente
     */
    async getByPaciente(pacienteId) {
        // TODO: Implementar cuando tengas el endpoint
        const key = `sr_historia_${pacienteId}`;
        return JSON.parse(localStorage.getItem(key) || '[]');
    },

    /**
     * Agregar entrada a historia clínica
     */
    async addEntrada(pacienteId, entrada) {
        // TODO: Implementar cuando tengas el endpoint
        const key = `sr_historia_${pacienteId}`;
        const historia = JSON.parse(localStorage.getItem(key) || '[]');
        const nuevaEntrada = {
            id: Date.now(),
            fecha: new Date().toISOString().split('T')[0],
            ...entrada
        };
        historia.push(nuevaEntrada);
        localStorage.setItem(key, JSON.stringify(historia));
        return nuevaEntrada;
    }
};

// =====================================================
// API DE DICCIONARIO MÉDICO (placeholder)
// =====================================================

const DiccionarioAPI = {
    /**
     * Obtener todos los términos
     */
    async getAll() {
        // TODO: Implementar cuando tengas el endpoint
        return [
            {
                id: 1,
                termino: 'Hipertensión',
                definicion: 'Elevación sostenida de la presión arterial.',
                causas: 'Genética, dieta alta en sal',
                tratamientos: 'Control de presión, dieta, medicación.'
            },
            {
                id: 2,
                termino: 'Gripe',
                definicion: 'Infección respiratoria viral.',
                causas: 'Virus Influenza',
                tratamientos: 'Reposo, líquidos, antipiréticos.'
            },
            {
                id: 3,
                termino: 'Diabetes',
                definicion: 'Afección caracterizada por glucosa elevada.',
                causas: 'Genética, obesidad',
                tratamientos: 'Control dietético, medicamentos.'
            }
        ];
    },

    /**
     * Buscar términos
     */
    async search(query) {
        const terminos = await this.getAll();
        const q = query.toLowerCase();
        return terminos.filter(t => 
            t.termino.toLowerCase().includes(q) ||
            t.definicion.toLowerCase().includes(q)
        );
    }
};

// =====================================================
// EXPORTAR MÓDULOS
// =====================================================

// Si usas módulos ES6
// export { UsuariosAPI, MedicosAPI, CitasAPI, AgendaAPI, HistoriaAPI, DiccionarioAPI, getCurrentUser, saveUser, logout, requireAuth, requireRole };

// Para uso directo en HTML (sin módulos)
window.API = {
    Usuarios: UsuariosAPI,
    Medicos: MedicosAPI,
    Citas: CitasAPI,
    Agenda: AgendaAPI,
    Historia: HistoriaAPI,
    Diccionario: DiccionarioAPI,
    getCurrentUser,
    saveUser,
    logout,
    requireAuth,
    requireRole
};
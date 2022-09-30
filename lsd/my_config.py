def lsd_cfg():
    resp = {
        'default': {
            'dia_base': 30,
            'forma_pago': 1,
            'ccn_sueldo': 'SUELDO',
            'ccn_no_rem': 'ASNORE',
            'ccn_no_osysind': 'ACUENR',
            'ccn_no_sind': 'PRUEBA',
            'ccn_sijp': 'JUBILA',
            'ccn_inssjp': 'INSSJP',
            'ccn_os': 'OBRSOC',
            'ccn_sindicato': 'SINDIC',
            'porc_sindicato': 4.5,
            'tipo_nr': 2,  # 0: Sólo NR, 1: Base Sindicato, 2: Base Sindicato y Obra Social
            'area': 'Administración',
            'cuit_empleador_eventuales': 30692273725,
        },
        'lugezz': {
            'dia_base': 30,
            'forma_pago': 1,
            'ccn_sueldo': '1000',
            'ccn_no_rem': '1500',
            'ccn_no_osysind': '1600',
            'ccn_no_sind': '1700',
            'ccn_sijp': '/321',
            'ccn_inssjp': '/351',
            'ccn_os': '/361',
            'ccn_sindicato': '2720',
            'porc_sindicato': 2,
            'tipo_nr': 0,  # 0: Sólo NR, 1: Base Sindicato, 2: Base Sindicato y Obra Social
            'area': 'Administración',
            'cuit_empleador_eventuales': 30692273725,
        },
    }

    return resp

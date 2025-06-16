
from mainfinal import es_duplicado
estudiantes = [{'legajo':11111, 'nombre':'leo Castillo','correo':'abc1@uade.edu.ar','materias':['fisica', 'progra1'],'fecha_baja':None},
                   {'legajo':11112, 'nombre':'caro Casto','correo':'abc2@uade.edu.ar','materias':['progra1'],'fecha_baja':None},
                   {'legajo':11113, 'nombre':'andres julio','correo':'abc3@uade.edu.ar','materias':None,'fecha_baja':None}]

def test_duplicados():
    assert es_duplicado('nombre','Leo Castillo',estudiantes)==True
    assert es_duplicado('nombre', 'ana torres',estudiantes)==False
    assert es_duplicado('correo','abc3@uade.edu.ar',estudiantes)==True
    assert es_duplicado('correo','abc4@uade.edu.ar',estudiantes)==False
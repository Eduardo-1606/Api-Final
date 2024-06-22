from flask import Flask, jsonify, request, abort
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker
import psycopg2

app = Flask(__name__)

engine = create_engine('postgresql+psycopg2://postgres:admin@localhost:5432/To-Do')
Base = declarative_base()

class Tarea(Base):
    __tablename__ = 'tareas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String, nullable=False)
    fecha_limite = Column(Date, nullable=False)

    def serialize(self):
        return{
            'id':self.id,
            'descripcion':self.descripcion,
            'fecha_limite': self.fecha_limite.isoformat()
        }
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/tareas', methods=['POST'])
def crear_tarea():
    if not request.is_json:
        return abort(400, 'Se espera JSON')
    descripcion = request.json.get('descripcion')
    fecha_limite = request.json.get('fecha_limite')

    if not descripcion or not fecha_limite:
        return abort(400, 'Faltan datos: descripcion y fecha_limite')
    
    nueva_tarea = Tarea(descripcion=descripcion, fecha_limite=fecha_limite)
    session =Session()
    session.add(nueva_tarea)
    session.commit()

    return jsonify({'tarea': nueva_tarea.serialize()}), 201

@app.route('/tareas', methods=['GET'])
def listar_tareas():
    session = Session()
    todas_las_tareas = session.query(Tarea).all()

    tareas_json = [tarea.serialize() for tarea in todas_las_tareas]
    return jsonify({'tarea': tareas_json})

@app.route ('/tareas', methods=['GET'])
def obtener_tarea(id):
    tarea = session.query(Tarea).get(id)
    if tarea:
        return jsonify({'id': tarea.id, 'descripcion': tarea.descripcion, 'fecha_limite':tarea.fecha_limite.isoformat()})
    else:
        return jsonify({'message': 'Tarea no encontrada'}), 400

@app.route('/tareas/<int:id>', methods=['DELETE'])
def eliminar_tarea(id):
    tarea = session.query(Tarea).get(id)
    if tarea:
        session.delete(tarea)
        session.commit()
        return jsonify({'mensaje': 'Tarea eliminada correctamente'})
    else:
        return jsonify({'message': 'Tarea no encontrada'}), 400

@app.route('/tareas/<int:id>', methods=['PUT'])
def modificar_tarea(id):
    data = request.json
    tarea = session.query(Tarea).get(id)
    
    if tarea:
        tarea.descripcion = data.get('descripcion', tarea.descripcion)
        tarea.fecha_limite = data.get('fecha_limite', tarea.fecha_limite)
        session.commit()
        return jsonify({'message':'Tarea realizada con exito'})
    else:
        return jsonify({'message': 'Tarea no encontrada'}), 400
    

def serialize(self):
    return{
        'id': self.id,
        'descripcion': self.descripcion,
        'fecha_limite': self.fecha_limite
    }

if __name__ == '__main__':
    app.run(debug=True)
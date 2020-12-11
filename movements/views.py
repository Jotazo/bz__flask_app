from movements import app
from flask import render_template, request, redirect, url_for
import csv
import sqlite3

@app.route('/')
def listaIngresos():

    conn = sqlite3.connect('movements/data/basededatos.db')
    c = conn.cursor()
    c.execute('SELECT fecha, concepto, cantidad, id FROM movimientos')
    ingresos = c.fetchall()
    conn.close()
    
    total = 0

    for ingreso in ingresos:
        total += ingreso[2]

    return render_template('movementsList.html', datos=ingresos, total=total)

@app.route('/creaalta', methods=['GET', 'POST'])
def nuevoIngreso():



    if request.method == 'POST':
        conn = sqlite3.connect('movements/data/basededatos.db')
        c = conn.cursor()
        c.execute('INSERT INTO movimientos(cantidad, concepto, fecha) VALUES(?,?,?)', 
                (
                    float(request.form.get('cantidad')), 
                    request.form.get('concepto'), 
                    request.form.get('fecha'),
                )
        )
        conn.commit()
        conn.close()
        return redirect(url_for('listaIngresos'))

    return render_template('alta.html')

@app.route('/modifica/<id>', methods=['GET', 'POST'])
def modificaIngreso(id):
    conn = sqlite3.connect('movements/data/basededatos.db')
    c = conn.cursor()

    if request.method == 'GET':
        c.execute('SELECT fecha, concepto, cantidad, id FROM movimientos WHERE id=?',id)
        registro = c.fetchone() 
        conn.close()

        return render_template('modifica.html', registros=registro)

    elif request.method == 'POST':
        fecha = request.form.get('fecha')
        concepto = request.form.get('concepto')
        cantidad = request.form.get('cantidad')
        idoculta = request.form.get('id')
        registro = (fecha, concepto, cantidad, idoculta)

        c.execute('UPDATE movimientos SET fecha=?, concepto=?, cantidad=? WHERE id=?', registro)
        conn.commit()
        conn.close()

        return redirect(url_for('listaIngresos'))

@app.route('/delete/<id>', methods=['GET', 'POST'])
def borraIngreso(id):
    conn = sqlite3.connect('movements/data/basededatos.db')
    c = conn.cursor()

    if request.method == 'GET':
        c.execute('SELECT fecha, concepto, cantidad, id FROM movimientos WHERE id=?', id)
        registroEliminar = c.fetchone()
        conn.close()

        return render_template('borraingreso.html', r=registroEliminar)

    if request.method == 'POST':
        c.execute('DELETE FROM movimientos WHERE id=?', request.form.get('id'))
        conn.commit()
        conn.close()

        return redirect(url_for('listaIngresos'))
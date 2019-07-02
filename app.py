# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 22:17:06 2019

@author: havana
"""

from flask import Flask

app = Flask(__name__)

@app.route("/")
def main():
    return "Welcome to my flask page!"

@app.route("/hi")
def hi():
    return "Hi"
    
def createGruposByTurma(id_turma,n_members):
    import horariosAtivos as hat
    rowCount = hat.criaCLustersBySchedule(id_turma,n_members)
    if rowCount == 0:
        return "Grupos criados com sucesso"
    else:
        return "Pobremas"

app.add_url_rule("/turma/<id_turma>/<n_members>/",view_func=createGruposByTurma,endpoint="id_turma")

#if __name__ == "__main__":
app.run()
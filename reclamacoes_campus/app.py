from flask import Flask, render_template, request, redirect
import model

app = Flask(__name__)

model.criar_banco()
model.criar_tabelas()


@app.route("/")
def index():
    reclamacoes = model.listar()
    return render_template(
        "index.html",
        reclamacoes=reclamacoes
    )


@app.route("/nova")
def nova():
    return render_template("nova.html")


@app.route("/salvar", methods=["POST"])
def salvar():
    titulo = request.form["titulo"]
    descricao = request.form["descricao"]
    categoria = request.form["categoria"]
    local = request.form["local"]

    model.inserir(
        titulo,
        descricao,
        categoria,
        local
    )

    return redirect("/")


@app.route("/admin")
def admin():
    reclamacoes = model.listar()
    return render_template(
        "admin.html",
        reclamacoes=reclamacoes
    )


@app.route("/status/<int:id>", methods=["POST"])
def status(id):
    novo_status = request.form["status"]

    model.atualizar_status(id, novo_status)

    return redirect("/admin")


@app.route("/excluir/<int:id>")
def excluir(id):
    model.excluir(id)

    return redirect("/admin")


if __name__ == "__main__":
    app.run(debug=True)

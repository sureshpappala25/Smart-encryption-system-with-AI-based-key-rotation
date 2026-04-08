from flask import Blueprint,request,render_template
from encryption.key_rotation import rotate_key

ai_bp = Blueprint("ai",__name__)

@ai_bp.route("/key_rotation",methods=["GET","POST"])
def key_rotation():

    if request.method=="POST":

        login_attempts = int(request.form["login"])
        data_access = int(request.form["access"])
        threat_score = float(request.form["threat"])

        result = rotate_key(login_attempts,data_access,threat_score)

        return render_template("result.html",result=result)

    return render_template("key_rotation.html")
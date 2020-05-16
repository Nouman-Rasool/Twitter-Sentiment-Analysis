from app import app

@app.route("/admin/dashboard")
def admin_dashboard():
	return "Admin dashbord is lovley"


@app.route("/admin/profile")
def profile():
    return "<h1>This my profile</h1>"
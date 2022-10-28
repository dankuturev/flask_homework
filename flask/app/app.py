from server import app
from adviews import AdViews

app.add_url_rule('/ads/', methods=['POST'], view_func=AdViews.as_view('create_ad'))
app.add_url_rule('/ads/<int:ad_id>', methods=['GET', 'PATCH', 'DELETE'], view_func=AdViews.as_view('get_ad'))
app.run()

from flask import Flask, render_template
from flask_material import Material
from plots import generate_plot
from queries import get_schema, get_price_for_nearest_date
from choromap import create_map

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def homepage():
	bar = create_map()
	return render_template("homepage.html", plot=bar)


@app.route("/visualization", methods=['GET', 'POST'])
@app.route("/visualization/<args>", methods=['GET', 'POST'])
def visualization(args = None):     
	area_list = get_schema()[1:] # We are only interested in columns containing area names.
	graph = generate_plot(args.split('+')) if args is not None else None

	return render_template("visualization.html", area_list=area_list, graph=graph)


@app.route("/priceSearch", methods=['GET', 'POST'])
@app.route("/priceSearch/<args>", methods=['GET', 'POST'])
def search_price(args = None):
	area_list = get_schema()[1:]
	q_result = ''

	if args is not None:
		db_args = args.split('+')
		q_val = get_price_for_nearest_date(fuel_type=db_args[0], area=db_args[1], date=db_args[2])
		q_result = f"Price of {db_args[0]} fuel in {db_args[1]} on {q_val[0]} is ${q_val[1]}." + ('' if q_val[2] == 0 else f" No result for {db_args[2]}.")
	
	return render_template("priceSearch.html", area_list=area_list, q_result=q_result)


if __name__ == "__main__":
	app.run()

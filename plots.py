import matplotlib.pyplot as plt
import io
import base64
from queries import getFuelPrice

def generate_plot(args):
	fig = plt.figure(figsize=(12,8))

	fig.patch.set_facecolor("white")
	fig.patch.set_alpha(0.7)

	ax = fig.add_subplot(111)

	img = io.BytesIO()

	fuel_type = args[0]
	areas = args[1:]
	for area in areas:
		data = getFuelPrice(area=area, fuel_type=fuel_type, period="annually")
		ax.plot(['\n'.join(d[0].split()) for d in data], [d[1] for d in data], ".-", label=area)

	plt.legend(loc="best")
	plt.title(f"Fuel type: {fuel_type}")
	plt.xlabel("Time in Years")
	plt.ylabel("Price in USD")
	plt.xticks(fontsize=7)

	ax.patch.set_facecolor("white")
	ax.patch.set_alpha(0.0)

	fig.savefig(img, format='png', facecolor=fig.get_facecolor(), edgecolor='none')

	img.seek(0)
	return base64.b64encode(img.getvalue()).decode()
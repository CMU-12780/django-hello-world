# Django Hello World

The PIT airport train facts app from the Django activity, set up to run in a dev container. Use it in place of your own `helloworld` project, or follow [Add a Chart](#add-a-chart) in yours.

## Run It

### In GitHub Codespaces

On this repository's page, choose **Code**, then **Codespaces**, then **Create codespace on main**. Setup installs Django, creates the database and loads four starter facts. When it finishes, run:

```bash
python manage.py runserver
```

Open the forwarded port 8000 when VS Code offers it.

### In VS Code With Docker

Install the Dev Containers extension, open this folder and choose **Reopen in Container**. Then run `python manage.py runserver` and open http://127.0.0.1:8000.

### Without a Container

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata facts
python manage.py runserver
```

### As a Docker Image

```bash
docker build -t django-hello-world .
docker run --rm -p 8000:8000 django-hello-world
```

## Pages

* `/`: Hello world page.
* `/facts/`: Every fact as JSON.
* `/random/`: A random fact.
* `/random.json`: A random fact as JSON.
* `/admin/`: Django admin.

To sign in to the admin, create a user first. This user exists only in your copy of the database:

```bash
python manage.py createsuperuser
```

## Add a Chart

These steps add a page at `/chart/` that charts how many facts were added each day with [Chart.js](https://www.chartjs.org/). They work in this repository or in your own `helloworld` project from the Django activity.

### 1. Write the View

Add this import to the top of `pittrain/views.py`:

```python
from django.db.models import Count
```

If you're working in your own project, also add `from django.shortcuts import render` if it isn't there.

Then add this view at the bottom. It counts the facts for each day and passes the dates and counts to the template:

```python
def facts_chart(request):
    rows = (
        PITAirportTrainFact.objects
        .values("dateAdded")
        .annotate(count=Count("id"))
        .order_by("dateAdded")
    )
    chart_data = {
        "labels": [row["dateAdded"].isoformat() for row in rows],
        "counts": [row["count"] for row in rows],
    }
    return render(request, "facts_chart.html", {"chart_data": chart_data})
```

### 2. Add the URL

In `pittrain/urls.py`, add this line to `urlpatterns`:

```python
path("chart/", views.facts_chart, name="facts_chart"),
```

### 3. Create the Template

Create `pittrain/templates/facts_chart.html`, making the `templates` folder if you don't have one. The `json_script` filter writes `chart_data` into the page as JSON, and the script reads it back to draw the chart:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Facts Added Per Day</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.6.1/dist/chart.umd.min.js"></script>
</head>
<body>
  <h1>Facts Added Per Day</h1>
  <canvas id="facts-chart"></canvas>
  {{ chart_data|json_script:"chart-data" }}
  <script>
    const chartData = JSON.parse(document.getElementById("chart-data").textContent);
    new Chart(document.getElementById("facts-chart"), {
      type: "bar",
      data: {
        labels: chartData.labels,
        datasets: [{ label: "Facts Added", data: chartData.counts }]
      },
      options: {
        scales: { y: { beginAtZero: true, ticks: { precision: 0 } } }
      }
    });
  </script>
</body>
</html>
```

### 4. Try It

Run the server and open `/chart/`. The starter facts all have the same date, so the chart starts with one bar. Add a fact in the admin and reload to see a bar for today.

### Troubleshooting

* **`TemplateDoesNotExist`:** Check that the template is in `pittrain/templates/` and that `"pittrain"` is in `INSTALLED_APPS` in `helloworld/settings.py`.
* **`Page not found (404)`:** Check that `helloworld/urls.py` includes `pittrain.urls` and that the address ends in `/chart/`.
* **A blank page with no chart:** Open your browser's developer tools and read the error in the console.
* **`DisallowedHost` or `CSRF verification failed` in your own project in Codespaces:** Copy `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` from this repository's `helloworld/settings.py` into yours.

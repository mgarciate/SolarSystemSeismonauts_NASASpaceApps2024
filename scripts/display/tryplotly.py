import plotly.graph_objects as go

# Datos ficticios de sismos
lats = [30, 50, 80, 40, 60]
lons = [70, 100, 130, 90, 120]
depths = [10, 30, 20, 50, 40]  # Profundidades en km
magnitudes = [3.5, 4.2, 5.1, 3.9, 4.7]  # Magnitudes de los sismos

# Crear gráfica en 3D
fig = go.Figure(data=[go.Scatter3d(
    x=lons, y=lats, z=depths,
    mode='markers',
    marker=dict(
        size=[m * 3 for m in magnitudes],
        color=depths,
        colorscale='Viridis',
        opacity=0.8
    )
)])

# Actualizar etiquetas y título
fig.update_layout(scene=dict(
                    xaxis_title='Longitud',
                    yaxis_title='Latitud',
                    zaxis_title='Profundidad'),
                  title="Sismos en Marte en 3D")
fig.show()
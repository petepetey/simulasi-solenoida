
import numpy as np
import math
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🧲 PROYEK ANALISIS VEKTOR")
st.markdown("### Penerapan: **Simulasi Induksi Elektromagnetik pada Solenoida Spiral**")

# Sidebar input
n = st.sidebar.slider("Jumlah lilitan (N)", 1, 100, 10)
r = st.sidebar.slider("Radius solenoida (cm)", 1.0, 5.0, 1.0)
h = st.sidebar.slider("Tinggi solenoida (cm)", 1.0, 20.0, 5.0)
B0 = st.sidebar.slider("Medan Magnet Maksimum B₀ (T)", 0.1, 10.0, 1.0)
f = st.sidebar.slider("Frekuensi (Hz)", 0.1, 10.0, 1.0)
t = st.sidebar.slider("Waktu (s)", 0.0, 1.0, 0.0, step=0.01)

# Konversi satuan
r_m = r / 100
A = math.pi * r_m**2
B_t = B0 * np.cos(2 * math.pi * f * t)
Phi_t = B_t * A
epsilon_t = 2 * math.pi * f * B0 * A * np.sin(2 * math.pi * f * t)

# Spiral kawat
theta = np.linspace(0, 2 * np.pi * n, 500)
z_spiral = np.linspace(0, h, 500)
x_spiral = r * np.cos(theta)
y_spiral = r * np.sin(theta)

spiral_trace = go.Scatter3d(
    x=x_spiral, y=y_spiral, z=z_spiral,
    mode='lines',
    line=dict(color='orange', width=4),
    name='Solenoida',
    hovertemplate="Solenoida<br>x: %{x:.2f}<br>y: %{y:.2f}<br>z: %{z:.2f}"
)

# Permukaan fluks
circle_theta = np.linspace(0, 2 * np.pi, 100)
circle_x = r * np.cos(circle_theta)
circle_y = r * np.sin(circle_theta)
circle_z = np.full_like(circle_theta, h / 2)

flux_surface = go.Scatter3d(
    x=circle_x, y=circle_y, z=circle_z,
    mode='lines',
    line=dict(color='deepskyblue', width=4),
    name='Fluks Magnetik',
    hovertemplate="Fluks<br>x: %{x:.2f}<br>y: %{y:.2f}<br>z: %{z:.2f}"
)

# Fluks luar
flux_lines = []
n_arah = 12
angles = np.linspace(0, 2 * np.pi, n_arah, endpoint=False)
for i, a in enumerate(angles):
    rx = r * np.cos(a)
    ry = r * np.sin(a)
    z_in = np.linspace(h/2 - 1, h/2 + 1, 10)
    flux_lines.append(go.Scatter3d(
        x=np.full_like(z_in, rx),
        y=np.full_like(z_in, ry),
        z=z_in,
        mode='lines',
        line=dict(color='skyblue', width=2),
        name='Fluks Luar' if i == 0 else None,
        showlegend=(i == 0),
        hoverinfo='skip' if i != 0 else 'all',
        hovertemplate="Fluks Luar<br>x: %{x}<br>y: %{y}<br>z: %{z}"
    ))

# Medan vektor
z_vec = np.linspace(h/2 - 0.8, h/2 + 0.8, 6)
cones = []
for zv in z_vec:
    cones.append(go.Cone(
        x=[0], y=[0], z=[zv],
        u=[0], v=[0], w=[B_t],
        sizemode='absolute', sizeref=0.25,
        anchor='tail', colorscale='Viridis',
        showscale=False,
        showlegend=False
    ))

# Gabungkan semua visual
fig = go.Figure(data=[spiral_trace, flux_surface] + flux_lines + cones)
fig.update_layout(
    title=f"t = {t:.2f} s | B(t) = {B_t:.3f} T",
    scene=dict(
        xaxis_title='X', yaxis_title='Y', zaxis_title='Z',
        bgcolor='rgba(10,10,20,0.95)',
        xaxis=dict(backgroundcolor='black', color='white', gridcolor='gray'),
        yaxis=dict(backgroundcolor='black', color='white', gridcolor='gray'),
        zaxis=dict(backgroundcolor='black', color='white', gridcolor='gray')
    ),
    margin=dict(l=0, r=0, b=0, t=40)
)

# Grafik fluks dan GGL
t_vals = np.linspace(0, 1 / f, 500)
phi_vals = B0 * np.cos(2 * np.pi * f * t_vals) * A
emf_vals = -np.gradient(phi_vals, t_vals)

fig_phi = go.Figure()
fig_phi.add_trace(go.Scatter(x=t_vals, y=phi_vals, mode='lines',
    name='Φ(t)', line=dict(color='limegreen', width=2),
    hovertemplate="t = %{x:.4f}s<br>Φ = %{y:.4e} Wb"))
fig_phi.update_layout(
    title="Fluks Magnetik Φ(t)",
    xaxis_title="Waktu (s)",
    yaxis_title="Fluks (Wb)",
    template="plotly_dark"
)

fig_emf = go.Figure()
fig_emf.add_trace(go.Scatter(x=t_vals, y=emf_vals, mode='lines',
    name='ε(t)', line=dict(color='crimson', width=2),
    hovertemplate="t = %{x:.4f}s<br>ε = %{y:.4f} V"))
fig_emf.update_layout(
    title="GGL Induksi ε(t)",
    xaxis_title="Waktu (s)",
    yaxis_title="Tegangan (V)",
    template="plotly_dark"
)

# Tampilkan
col1, col2 = st.columns([1, 2])
with col1:
    st.markdown(f"**Medan Magnet B(t)** = `{B_t:.4f} T`")
    st.markdown(f"**Fluks Magnetik Φ(t)** = `{Phi_t:.6f} Weber`")
    st.markdown(f"**GGL Induksi ε(t)** = `{epsilon_t:.6f} Volt`")
with col2:
    st.plotly_chart(fig, use_container_width=True)

st.subheader("📈 Grafik Fluks Magnetik dan GGL Induksi")
col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(fig_phi, use_container_width=True)
with col4:
    st.plotly_chart(fig_emf, use_container_width=True)

# Info penyusun
st.markdown("---")
st.markdown("""
#### Disusun oleh  
**Peter Immanuel Sitompul**  
NIM: `21060124130049`
""")

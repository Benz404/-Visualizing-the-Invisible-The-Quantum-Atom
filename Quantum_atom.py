import pygame
import pygame_gui
import math
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

# --- Constants ---
WIDTH, HEIGHT = 1300, 850
# Pygame Colors (0-255)
PY_BLUE = (100, 150, 255)
PY_RED = (255, 80, 80)

# Matplotlib Colors (0.0-1.0)
MPL_BLUE = (100/255, 150/255, 255/255)
MPL_RED = (255/255, 80/255, 80/255)

class QuantumVsBohrLab:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Quantum vs Bohr Laboratory - Resizable")
        # Enable Resizable Window
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.n = 3
        self.l = 0
        self.points = []
        
        # UI Elements
        self.setup_ui()
        
        # Separate plotting for Bohr and Quantum
        self.fig_bohr, self.ax_bohr = plt.subplots(figsize=(4, 2.5), dpi=100)
        self.fig_quant, self.ax_quant = plt.subplots(figsize=(4, 2.5), dpi=100)
        
        self.update_all()

    def setup_ui(self):
        w, h = self.screen.get_size()
        # Anchoring sliders to the bottom right
        self.n_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((w - 320, h - 180), (280, 25)),
            start_value=3, value_range=(1, 4), manager=self.manager)
        
        self.l_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((w - 320, h - 110), (280, 25)),
            start_value=0, value_range=(0, 3), manager=self.manager)
        
        self.n_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((w - 320, h - 210), (280, 30)),
            text=f"Energy Level (n): {self.n}", manager=self.manager)
        
        self.l_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((w - 320, h - 140), (280, 30)),
            text=f"Orbital Shape (l): s", manager=self.manager)

    def get_quantum_radial(self, r, n, l):
        """Standard Hydrogen-like Radial Probability Density"""
        # Simplification of Laguerre polynomials to show 'bumps/nodes'
        if n == 1: return (r**2) * np.exp(-r)
        if n == 2:
            if l == 0: return (r**2) * ((2 - r)**2) * np.exp(-r)
            return (r**4) * np.exp(-r)
        if n == 3:
            if l == 0: return (r**2) * (6 - 6*r + r**2)**2 * np.exp(-r)
            if l == 1: return (r**4) * (4 - r)**2 * np.exp(-r)
            return (r**6) * np.exp(-r)
        if n == 4:
            if l == 0: return (r**2) * (24 - 36*r + 12*r**2 - r**3)**2 * np.exp(-r)
            return (r**4) * (10 - r)**2 * np.exp(-r)
        return 0

    def plot_graphs(self):
        r_vals = np.linspace(0, 25, 200)

        # 1. Bohr Graph
        self.ax_bohr.clear()
        bohr_r = self.n**2 * 0.8 # Scaling for visual clarity
        bohr_p = np.exp(-(r_vals - bohr_r)**2 / 0.5)
        self.ax_bohr.plot(r_vals, bohr_p, color=MPL_RED, lw=2)
        self.ax_bohr.set_title("Bohr Model (Single Peak)", color='white', fontsize=10)
        self.style_plot(self.ax_bohr, self.fig_bohr)

        # 2. Quantum Graph (The Bumps/Nodes)
        self.ax_quant.clear()
        p_vals = [self.get_quantum_radial(r, self.n, self.l) for r in r_vals]
        p_vals = p_vals / np.max(p_vals) if np.max(p_vals) > 0 else p_vals
        self.ax_quant.plot(r_vals, p_vals, color=MPL_BLUE, lw=2)
        self.ax_quant.fill_between(r_vals, p_vals, color=MPL_BLUE, alpha=0.3)
        self.ax_quant.set_title(f"Quantum Model (Radial Nodes: {self.n - self.l - 1})", color='white', fontsize=10)
        self.style_plot(self.ax_quant, self.fig_quant)

        self.bohr_surf = self.render_to_surf(self.fig_bohr)
        self.quant_surf = self.render_to_surf(self.fig_quant)

    def style_plot(self, ax, fig):
        ax.set_facecolor('#101015')
        fig.patch.set_facecolor('#101015')
        ax.tick_params(colors='white', labelsize=7)
        for spine in ax.spines.values(): spine.set_color('#444444')

    def render_to_surf(self, fig):
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        return pygame.image.frombuffer(canvas.buffer_rgba(), canvas.get_width_height(), "RGBA")

    def generate_cloud(self):
        self.points = []
        count = 4500
        while len(self.points) < count:
            r = random.uniform(0, 30)
            theta = random.uniform(0, math.pi)
            phi = random.uniform(0, 2 * math.pi)
            
            p_r = self.get_quantum_radial(r, self.n, self.l)
            if self.l == 0: p_a = 1.0
            elif self.l == 1: p_a = math.cos(theta)**2
            elif self.l == 2: p_a = (3*math.cos(theta)**2 - 1)**2
            else: p_a = (math.cos(theta)*(5*math.cos(theta)**2-3))**2
            
            if random.random() < (p_r * p_a * 1.5):
                x = r * math.sin(theta) * math.cos(phi)
                y = r * math.sin(theta) * math.sin(phi)
                z = r * math.cos(theta)
                self.points.append([x, y, z])

    def update_all(self):
        self.generate_cloud()
        self.plot_graphs()

    def run(self):
        angle_y, angle_x = 0, 0
        running = True
        while running:
            time_delta = self.clock.tick(60)/1000.0
            w, h = self.screen.get_size()
            self.screen.fill((5, 5, 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                if event.type == pygame.VIDEORESIZE:
                    # Sync UI Manager with new window size
                    self.manager.set_window_resolution((event.w, event.h))
                    # Relocate UI Elements
                    self.n_slider.set_relative_position((event.w - 320, event.h - 180))
                    self.l_slider.set_relative_position((event.w - 320, event.h - 110))
                    self.n_label.set_relative_position((event.w - 320, event.h - 210))
                    self.l_label.set_relative_position((event.w - 320, event.h - 140))
                
                if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    self.n = int(self.n_slider.get_current_value())
                    self.l = min(int(self.l_slider.get_current_value()), self.n - 1)
                    l_names = ["s-orbital", "p-orbital", "d-orbital", "f-orbital"]
                    self.n_label.set_text(f"Energy Level (n): {self.n}")
                    self.l_label.set_text(f"Orbital Shape (l): {l_names[self.l]}")
                    self.update_all()
                self.manager.process_events(event)

            angle_y += 0.01; angle_x += 0.005
            sim_center = (w // 3, h // 2)
            pygame.draw.circle(self.screen, PY_RED, sim_center, 6)

            for p in self.points:
                x, y, z = p
                ry_x = x * math.cos(angle_y) - z * math.sin(angle_y)
                ry_z = x * math.sin(angle_y) + z * math.cos(angle_y)
                rx_y = y * math.cos(angle_x) - ry_z * math.sin(angle_x)
                rx_z = y * math.sin(angle_x) + ry_z * math.cos(angle_x)
                
                scale = h / 45
                sx, sy = int(sim_center[0] + ry_x * scale), int(sim_center[1] + rx_y * scale)
                
                bright = max(0, min(255, int(180 - (rx_z * 8))))
                if 0 <= sx < w and 0 <= sy < h:
                    self.screen.set_at((sx, sy), (max(0, bright-100), max(0, bright-40), bright))

            # Render Graphs
            self.screen.blit(self.bohr_surf, (w - 450, 50))
            self.screen.blit(self.quant_surf, (w - 450, 320))
            
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    QuantumVsBohrLab().run()

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import japanize_matplotlib
from matplotlib.widgets import Button, Slider
from matplotlib.animation import FuncAnimation
import random

class VectorSpaceAdventure:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(12, 10))
        self.fig.suptitle('Vector Space Adventure', fontsize=16, fontweight='bold')

        self.level = 1
        self.score = 0
        self.player_vector = np.array([1, 1])
        self.target_vector = np.array([3, 2])
        self.basis_vectors = [np.array([1, 0]), np.array([0, 1])]
        self.current_combination = [1, 1]

        self.colors = {
                'player': '#FF6B6B',
                'target': '#4ECDC4',
                'basis': ['#FFF66D', '#FF8C42'],
                'grid': '#E8E8E8',
                'combination': '#A8E6CF'
        }

        #UI
        self.setup_ui()
        self.setup_level()

    def setup_ui(self):
        """UIコンポーネントの設定"""
        self.ax.set_xlim(-6, 6)
        self.ax.set_ylim(-6, 6)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3, color=self.colors['grid'])
        self.ax.axhline(y=0, color='k', linewidth=0.5)
        self.ax.axvline(x=0, color='k', linewidth=0.5)

        plt.subplots_adjust(bottom=0.25, right=0.85)

        ax_coef1 = plt.axes([0.1, 0.15, 0.3, 0.03])
        ax_coef2 = plt.axes([0.1, 0.1, 0.3, 0.03])

        self.slider_coef1 = Slider(ax_coef1, 'a1', -5, 5, valinit=1, valfmt='%.1f')
        self.slider_coef2 = Slider(ax_coef2, 'a2', -5, 5, valinit=1, valfmt='%.1f')

        #button
        ax_next = plt.axes([0.45, 0.15, 0.1, 0.04])
        ax_reset = plt.axes([0.45, 0.1, 0.1, 0.04])
        ax_hint = plt.axes([0.45, 0.05, 0.1, 0.04])

        self.btn_next = Button(ax_next, 'Next Level')
        self.btn_reset = Button(ax_reset, 'Reset')
        self.btn_hint = Button(ax_hint, 'Hint')

        #Event handler
        self.slider_coef1.on_changed(self.update_combination)
        self.slider_coef2.on_changed(self.update_combination)
        self.btn_next.on_clicked(self.next_level)
        self.btn_reset.on_clicked(self.reset_level)
        self.btn_hint.on_clicked(self.show_hint)

        self.info_text = self.fig.text(0.87, 0.8, '', fontsize=10, verticalalignment='top')

    def setup_level(self):
        if self.level == 1:
            self.target_vector = np.array([2, 3])
            self.basis_vectors = [np.array([1, 0]), np.array([0, 1])]
            self.level_description = "標準基底e1, e2を使って\n目標ベクトル(緑)に到達しよう!"
        elif self.level == 2:
            self.target_vector = np.array([1, 3])
            self.basis_vectors = [np.array([1, 1], np.array([1, -1]))]
            self.level_description = "新しい基底v1, v2を使って\n目標ベクトルを表現しよう!"

        elif self.level == 3:
            self.target_vector = np.array([4, 2])
            self.basis_vectors = [np.array([2, 1]), np.array([1, 2])]
            self.level_description = "異なる基底での\n線形結合を探そう!"
        else:
            angle1 = random.uniform(0, 2 * np.pi)
            angle2 = random.uniform(0, 2 * np.pi)
            self.basis_vectors = [
                    2 * np.array([np.cos(angle1), np.sin(angle1)]),
                    2 * np.array([np.cos(angle2), np.sin(angle2)])
            ]
            self.target_vector = np.random.uniform(-4, 4, 2)
            self.level_description = f"Level {self.level}\nランダム基底でチャレンジ!"
        self.update_display()
    
    def update_combination(self, val):
        self.current_combination = [self.slider_coef1.val, self.slider_coef2.val]
        self.player_vector = (self.current_combination[0] * self.basis_vectors[0] + self.current_combination[1] * self.basis_vectors[1])
        self.update_display()
        self.check_solution()

    def update_display(self):
        self.ax.clear()
        self.ax.set_xlim(-6, 6)
        self.ax.set_ylim(-6, 6)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3, color=self.colors['grid'])
        self.ax.axhline(y=0, color='k', linewidth=0.5)
        self.ax.axvline(x=0, color='k', linewidth=0.5)

        for i, basis in enumerate(self.basis_vectors):
            self.ax.arrow(0, 0, basis[0], basis[1],
                    head_width=0.15, head_length=0.15,
                    fc=self.colors['basis'][i],
                    ec=self.colors['basis'][i],
                    linewidth=2, alpha=0.8)
            self.ax.text(basis[0]*1.1, basis[1]*1.1, f'v1' if i==0 else'v2',
                    fontsize=12, fontweight='bold',
                    color=self.colors['basis'][i])

        coef1_vec = self.current_combination[0] * self.basis_vectors[0]
        coef2_vec = self.current_combination[1] * self.basis_vectors[1]

        if abs(self.current_combination[0]) > 0.1:
            self.ax.arrow(0, 0, coef1_vec[0], coef1_vec[1],
                    head_width=0.1, head_length=0.1,
                    fc=self.colors['basis'][0],
                    ec=self.colors['basis'][0],
                    linewidth=1, alpha=0.5, linestyle='--')

        if abs(self.current_combination[1]) > 0.1:
            self.ax.arrow(0, 0, coef2_vec[0], coef2_vec[1],
                    head_width=0.1, head_length=0.1,
                    fc=self.colors['basis'][1],
                    ec=self.colors['basis'][1],
                    linewidth=1, alpha=0.5, linestyle='--')

        if abs(self.current_combination[0]) > 0.1 and abs(self.current_combination[1]) > 0.1:
            parallelogram = patches.Polygon([
                [0, 0], coef1_vec, self.player_vector, coef2_vec], closed=True, fill=False, edgecolor=self.colors['combination'],
                linewidth=1, linestyle=':', alpha=0.7)
            self.ax.add_patch(parallelogram)

        self.ax.arrow(0, 0, self.player_vector[0], self.player_vector[1],
                head_width=0.2, head_length=0.2,
                fc=self.colors['player'],
                ec=self.colors['player'],linewidth=3)

        self.ax.arrow(0, 0, self.target_vector[0], self.target_vector[1],
                head_width=0.2, head_length=0.2,
                fc=self.colors['target'],
                ec=self.colors['target'],
                linewidth=3, alpha=0.8)

        self.ax.text(self.player_vector[0]*1.1, self.player_vector[1]*1.1,
                'Player', fontsize=10,
                color=self.colors['player'], fontweight='bold')
        self.ax.text(self.target_vector[0]*1.1, self.target_vector[1]*1.1,
                'Target', fontsize=10,
                color=self.colors['target'], fontweight='bold')

        distance = np.linalg.norm(self.player_vector - self.target_vector)
        info = f"Level: {self.level}\nScore: {self.score}\n\n"
        info += f"{self.level_description}\n\n"
        info += f"Linear Combination:\n"
        info += f"{self.current_combination[0]:.1f} x v1 + {self.current_combination[1]:.1f} x v2\n\n"
        info += f"Player: ({self.player_vector[0]:.1f}, {self.player_vector[1]:.1f})\n"
        info += f"Distance: {distance:.2f}"

        self.info_text.set_text(info)

        plt.draw()

    def check_solution(self):
        distance = np.linalg.norm(self.player_vector - self.target_vector)
        if distance < 0.2:
            self.score += max(100 - int(distance * 100), 50)
            self.ax.text(0, 5, 'SUCCESS!', fontsize=20, ha='center', color='green', fontweight='bold', bbox=dict(boxstyle="round,pad=0.3",facecolor="lightgreen", alpha=0.8))
            plt.draw()

    def next_level(self, event):
        self.level += 1
        self.setup_level()
        self.slider_coef1.reset()
        self.slider_coef2.reset()

    def reset_level(self, event):
        self.slider_coef1.reset()
        self.slider_coef2.reset()
        self.current_combination = [1, 1]
        self.update_display()

    def show_hint(self, event):
        try:
            basis_matrix = np.column_stack(self.basis_vectors)
            coefficients = np.linalg.solve(basis_matrix, self.target_vector)
            hint_text = f"Hint: 係数は約({coefficients[0]:.1f}, {coefficients[1]:.1f})"
            self.ax.text(0, -5, hint_text, fontsize=12, ha='center', bbox=dict(boxstyle="round,pad=0.3",facecolor="yellow", alpha=0.8))
            plt.draw()
        except np.linalg.LinAlgError:
            self.ax.text(0, -1, "Hint: この基底では表現できません!", fontsize=12, ha='center', bbox=dict(boxstyle="round,pad=0.3",facecolor="orange", alpha=0.8))
            plt.draw()

    def run(self):
        plt.show()

if __name__ == "__main__":
    game = VectorSpaceAdventure()
    game.run()


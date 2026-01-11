from manim import *
import numpy as np

class BubbleSortVisualization(Scene):
    def construct(self):
        # Konfiguracja
        self.bar_width = 0.7
        self.bar_spacing = 0.1
        self.base_y = -2.5
        values = [5, 3, 8, 1, 9, 2, 7, 4]
        n = len(values)
        
        # Tytuł
        title = Text("Bubble Sort", font_size=48, color=BLUE)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        
        # Złożoność
        complexity = MathTex(r"O(n^2)", font_size=36, color=YELLOW)
        complexity.next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(complexity))
        
        # Tworzenie słupków
        bars, labels = self.create_bars_with_labels(values)
        
        self.play(
            LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in bars], lag_ratio=0.1),
            run_time=1.5
        )
        self.play(LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.05))
        self.wait(0.5)
        
        # Licznik porównań i zamian
        comparisons = 0
        swaps = 0
        counter_text = always_redraw(
            lambda: Text(f"Porównania: {comparisons}  |  Zamiany: {swaps}", 
                        font_size=24, color=WHITE).to_edge(DOWN, buff=0.3)
        )
        self.add(counter_text)
        
        # Bubble Sort
        for i in range(n - 1):
            swapped = False
            for j in range(n - 1 - i):
                # Podświetl porównywane elementy
                self.play(
                    bars[j].animate.set_fill(RED, opacity=0.9),
                    bars[j+1].animate.set_fill(RED, opacity=0.9),
                    run_time=0.2
                )
                comparisons += 1
                
                if values[j] > values[j + 1]:
                    # Zamiana
                    swaps += 1
                    swapped = True
                    
                    # Animacja zamiany
                    self.swap_bars(bars, labels, j, j + 1, values)
                
                # Przywróć kolor
                self.play(
                    bars[j].animate.set_fill(BLUE, opacity=0.8),
                    bars[j+1].animate.set_fill(BLUE, opacity=0.8),
                    run_time=0.15
                )
            
            # Oznacz posortowany element
            self.play(bars[n-1-i].animate.set_fill(GREEN, opacity=0.9), run_time=0.2)
            
            if not swapped:
                break
        
        # Oznacz pozostałe jako posortowane
        for bar in bars:
            if bar.get_fill_color() != GREEN:
                self.play(bar.animate.set_fill(GREEN, opacity=0.9), run_time=0.1)
        
        # Końcowy tekst
        final_text = Text("Posortowano!", font_size=40, color=GREEN)
        final_text.next_to(counter_text, UP, buff=0.3)
        self.play(FadeIn(final_text, shift=UP))
        self.wait(2)

    def create_bars_with_labels(self, values):
        bars = VGroup()
        labels = VGroup()
        max_val = max(values)
        total_width = len(values) * (self.bar_width + self.bar_spacing) - self.bar_spacing
        start_x = -total_width / 2
        
        for i, val in enumerate(values):
            height = (val / max_val) * 3.5
            bar = Rectangle(
                width=self.bar_width,
                height=height,
                fill_color=BLUE,
                fill_opacity=0.8,
                stroke_color=WHITE,
                stroke_width=2
            )
            x_pos = start_x + i * (self.bar_width + self.bar_spacing) + self.bar_width/2
            bar.move_to([x_pos, self.base_y + height/2, 0])
            bars.add(bar)
            
            label = Text(str(val), font_size=24, color=WHITE)
            label.next_to(bar, UP, buff=0.1)
            labels.add(label)
        
        return bars, labels

    def swap_bars(self, bars, labels, i, j, values):
        values[i], values[j] = values[j], values[i]
        
        pos_i = bars[i].get_center()[0]
        pos_j = bars[j].get_center()[0]
        
        path_up = ArcBetweenPoints(
            bars[i].get_center(), 
            [pos_j, bars[i].get_center()[1], 0],
            angle=-PI/3
        )
        path_down = ArcBetweenPoints(
            bars[j].get_center(), 
            [pos_i, bars[j].get_center()[1], 0],
            angle=PI/3
        )
        
        self.play(
            MoveAlongPath(bars[i], path_up),
            MoveAlongPath(bars[j], path_down),
            labels[i].animate.move_to([pos_j, labels[i].get_center()[1], 0]),
            labels[j].animate.move_to([pos_i, labels[j].get_center()[1], 0]),
            run_time=0.4
        )
        
        # Zamień referencje w listach
        bars[i], bars[j] = bars[j], bars[i]
        labels[i], labels[j] = labels[j], labels[i]


class QuickSortVisualization(Scene):
    def construct(self):
        self.bar_width = 0.65
        self.bar_spacing = 0.12
        self.base_y = -2.5
        self.values = [6, 3, 8, 1, 9, 2, 7, 5]
        self.n = len(self.values)
        
        # Tytuł
        title = Text("Quick Sort", font_size=48, color=BLUE)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        
        # Złożoność
        complexity = MathTex(r"\text{Avg: } O(n \log n), \text{ Worst: } O(n^2)", font_size=32, color=YELLOW)
        complexity.next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(complexity))
        
        # Tworzenie słupków
        self.bars, self.labels = self.create_bars_with_labels()
        
        self.play(
            LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in self.bars], lag_ratio=0.1),
            run_time=1.5
        )
        self.play(LaggedStart(*[FadeIn(l) for l in self.labels], lag_ratio=0.05))
        self.wait(0.5)
        
        # Legenda
        legend = VGroup(
            VGroup(Square(0.3, fill_color=YELLOW, fill_opacity=0.8), Text("Pivot", font_size=20)).arrange(RIGHT, buff=0.1),
            VGroup(Square(0.3, fill_color=RED, fill_opacity=0.8), Text("Porównywany", font_size=20)).arrange(RIGHT, buff=0.1),
            VGroup(Square(0.3, fill_color=GREEN, fill_opacity=0.8), Text("Posortowany", font_size=20)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        legend.to_corner(UL, buff=0.5).shift(DOWN*0.8)
        self.play(FadeIn(legend))
        
        # Quick Sort
        self.quick_sort(0, self.n - 1)
        
        # Końcowa animacja
        self.play(
            *[bar.animate.set_fill(GREEN, opacity=0.9) for bar in self.bars],
            run_time=0.5
        )
        
        final_text = Text("Posortowano!", font_size=40, color=GREEN)
        final_text.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(final_text, shift=UP))
        self.wait(2)

    def create_bars_with_labels(self):
        bars = VGroup()
        labels = VGroup()
        max_val = max(self.values)
        total_width = self.n * (self.bar_width + self.bar_spacing) - self.bar_spacing
        start_x = -total_width / 2
        
        for i, val in enumerate(self.values):
            height = (val / max_val) * 3.5
            bar = Rectangle(
                width=self.bar_width,
                height=height,
                fill_color=BLUE,
                fill_opacity=0.8,
                stroke_color=WHITE,
                stroke_width=2
            )
            x_pos = start_x + i * (self.bar_width + self.bar_spacing) + self.bar_width/2
            bar.move_to([x_pos, self.base_y + height/2, 0])
            bars.add(bar)
            
            label = Text(str(val), font_size=24, color=WHITE)
            label.next_to(bar, UP, buff=0.1)
            labels.add(label)
        
        return bars, labels

    def quick_sort(self, low, high):
        if low < high:
            pivot_idx = self.partition(low, high)
            
            # Oznacz pivot jako posortowany
            self.play(self.bars[pivot_idx].animate.set_fill(GREEN, opacity=0.9), run_time=0.3)
            
            self.quick_sort(low, pivot_idx - 1)
            self.quick_sort(pivot_idx + 1, high)

    def partition(self, low, high):
        pivot = self.values[high]
        
        # Podświetl pivot
        self.play(self.bars[high].animate.set_fill(YELLOW, opacity=0.9), run_time=0.3)
        
        pivot_label = Text("pivot", font_size=20, color=YELLOW)
        pivot_label.next_to(self.bars[high], DOWN, buff=0.1)
        self.play(FadeIn(pivot_label))
        
        i = low - 1
        
        for j in range(low, high):
            # Podświetl porównywany element
            self.play(self.bars[j].animate.set_fill(RED, opacity=0.9), run_time=0.2)
            
            if self.values[j] <= pivot:
                i += 1
                if i != j:
                    self.swap(i, j)
                else:
                    self.play(self.bars[j].animate.set_fill(TEAL, opacity=0.8), run_time=0.15)
            else:
                self.play(self.bars[j].animate.set_fill(BLUE, opacity=0.8), run_time=0.15)
        
        # Zamień pivot na właściwe miejsce
        self.play(FadeOut(pivot_label))
        if i + 1 != high:
            self.swap(i + 1, high)
        
        return i + 1

    def swap(self, i, j):
        """Animacja zamiany"""
        self.values[i], self.values[j] = self.values[j], self.values[i]
        
        pos_i = self.bars[i].get_center()[0]
        pos_j = self.bars[j].get_center()[0]
        
        self.play(
            self.bars[i].animate.move_to([pos_j, self.bars[i].get_center()[1], 0]),
            self.bars[j].animate.move_to([pos_i, self.bars[j].get_center()[1], 0]),
            self.labels[i].animate.move_to([pos_j, self.labels[i].get_center()[1], 0]),
            self.labels[j].animate.move_to([pos_i, self.labels[j].get_center()[1], 0]),
            run_time=0.35
        )
        
        self.bars[i], self.bars[j] = self.bars[j], self.bars[i]
        self.labels[i], self.labels[j] = self.labels[j], self.labels[i]
        
        # Przywróć kolory
        self.play(
            self.bars[i].animate.set_fill(TEAL, opacity=0.8),
            self.bars[j].animate.set_fill(BLUE, opacity=0.8),
            run_time=0.15
        )
import matplotlib as plt
def plot_graph(self, v_color, e_color):
      for idx, v in enumerate(self.vertex):
            y, x = v.key
            plt.scatter(x, y, c=v_color)
            for n_idx, _ in self.neighbours(idx):
                yn, xn = self.getVertex(n_idx).key
                plt.plot([x, xn], [y, yn], color=e_color)
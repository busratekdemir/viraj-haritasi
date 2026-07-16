import sys

import cv2
import folium
import matplotlib
import numpy as np
import pandas as pd
import plotly
import scipy
import seaborn
import sklearn


def main():
    print("Viraj Haritası geliştirme ortamı hazır.")
    print(f"Python: {sys.version}")
    print(f"OpenCV: {cv2.__version__}")
    print(f"NumPy: {np.__version__}")
    print(f"Pandas: {pd.__version__}")
    print(f"SciPy: {scipy.__version__}")
    print(f"Scikit-learn: {sklearn.__version__}")
    print(f"Matplotlib: {matplotlib.__version__}")
    print(f"Plotly: {plotly.__version__}")
    print(f"Seaborn: {seaborn.__version__}")
    print(f"Folium: {folium.__version__}")


if __name__ == "__main__":
    main()
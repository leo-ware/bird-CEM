from data.make_grid import *

def test_assign_birds():
    assign_birds(np.array([0, 1, 2, 3, 4]), np.array([0, 1, 2, 3, 4]), "GB")
    # assign_birds(np.array([0, 1, 2, 3, 4]), np.array([0, 1, 2, 3, 4]), "US")

def test_create_grid_points():
    create_grid_points("GB", 1)
    # create_grid_points("US", 1)

def test_make_grid():
    make_grid("GB", 1)
    # make_grid("US", 10)

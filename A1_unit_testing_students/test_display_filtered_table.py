from products import *
import os, shutil, pytest

# inputs:
# open(csv_filename, 'r', newline='') as csvfile
# display_filtered_table(csv_filename, search)

@pytest.fixture(scope='module')
def copy_csv_file():
    shutil.copy('products.csv', 'copy_products.csv')
    print("\n----------------setup----------------\n")
    yield
    os.remove('copy_products.csv')
    print("\n----------------teardown----------------\n")

# Test a non-existing file
def test_EC1():
    assert display_filtered_table("non_existing_file.csv", "Apple")

# Test an empty csv file
def test_EC2(capsys):
    display_filtered_table("test_display_filtered_table_files/test_empty.csv", "Apple")
    out, err = capsys.readouterr()
    assert out == ""

# Test an empty string as csv file input
def test_EC3():
    assert display_filtered_table("", "Apple")

# Test an empty string as search input
def test_EC4(capsys, copy_csv_file):
    display_filtered_table("copy_products.csv", "")
    out, err = capsys.readouterr()
    assert out == ""

def test_EC5(capsys):
    display_filtered_table("test_files/test_1_column.csv")
    out, err = capsys.readouterr()
    assert out == ""


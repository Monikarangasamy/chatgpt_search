

# India Heatmap Generator 🗺️

A Python script that generates a geographic heatmap of India, visualizing per capita data for each state. This project uses the `geopandas` and `matplotlib` libraries to merge geospatial data with statistical information and create a visually appealing map.

-----

## Installation

Before running the script, you'll need to install the required Python libraries. You can do this by running the following command in your terminal or notebook environment:

```bash
pip install geopandas pandas matplotlib mapclassify
```

-----

<img width="1600" height="799" alt="image" src="https://github.com/user-attachments/assets/d589867b-55f9-467a-9f70-a09e61f33414" />


## Usage

To generate the heatmap, you must have two data files and a shapefile of India. The paths to these files are specified in the script and need to be updated to match your local file structure.

1.  **Update File Paths:**

      - `shapefile_path`: Path to your India shapefile directory.
      - `data1_path`: Path to your first CSV file with state-wise data.
      - `data2_path`: Path to your second CSV file with state-wise data.

2.  **Run the Script**:
    Execute the `heatmap.py` script. The program will process the data, handle geospatial complexities (like merging the geometries of Jammu & Kashmir and Ladakh), and display the final heatmap.

<!-- end list -->

```bash
python heatmap.py
```

### Example

The script processes two CSV files and a shapefile to produce a final image like this: .

The generated heatmap will display states colored by their "Per\_Capita\_Stat" value, with state names and corresponding values overlaid on the map for easy interpretation.

-----

## Features ✨

  * **Geospatial Data Merging**: Combines statistical data from CSV files with geographical shapefiles.
  * **State Name Standardization**: Cleans and standardizes state names to ensure accurate data merging.
  * **Geometrical Unification**: Corrects the representation of Jammu & Kashmir and Ladakh by merging their geometries.
  * **Dynamic Data Visualization**: Generates a customizable heatmap with a color bar and state-specific labels.
  * **Automated Label Placement**: Uses offsets to prevent text labels from overlapping with state borders, improving readability.

-----

## Project Structure

The project has a simple structure, with all core logic contained within a single Python script.

```
.
└── heatmap.py
```

-----

## Dependencies

This project relies on the following Python libraries:

  * **geopandas**: For working with geospatial data.
  * **pandas**: For data manipulation and analysis.
  * **matplotlib**: For creating the heatmap plot.
  * **mapclassify**: For classifying data into quantiles for plotting.
  * **shapely**: For geometric operations.

-----

## Contribution Guidelines

Feel free to fork this repository and submit pull requests with improvements. You can also open an issue if you encounter any bugs or have suggestions for new features.

-----

## License

This project is licensed under the **MIT License**.

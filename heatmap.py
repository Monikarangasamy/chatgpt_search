# Install necessary libraries if not installed
!pip install geopandas pandas matplotlib mapclassify

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
#from shapely.geometry import unary_union
from shapely.ops import unary_union  # Corrected import
from shapely import make_valid
from shapely.validation import make_valid, explain_validity
from shapely.geometry import Polygon

# 📌 Load India map (Shapefile)
shapefile_path = "/content/shape"  # Update with correct path
india_map = gpd.read_file(shapefile_path)

# 📌 Load per capita statistics data
data1_path = "/content/state_value/state_value_2_combine.csv"  # Update path
data2_path = "/content/state_value/geo_data_5_combine.csv"

data1 = pd.read_csv(data1_path)
data2 = pd.read_csv(data2_path)

# 📌 Standardize State Names
state_name_map = {
    "jammu & kashmir": "jammu and kashmir",
    "j & k": "jammu and kashmir",
    "ladakh": "ladakh",
    "chattisgarh": "chhattisgarh",
    "dadra and nagar haveli": "DNH",
    "daman and diu": "DND",
}

def clean_state_names(df, column):
    df[column] = df[column].str.strip().str.lower()
    df[column] = df[column].replace(state_name_map)

clean_state_names(india_map, 'st_nm')
clean_state_names(data1, 'st_nm')
clean_state_names(data2, 'st_nm')

# 📌 Merge data files
merged_data = pd.merge(data1, data2, on='st_nm', how='outer')

# 📌 Manually Set Per Capita Value for Jammu & Kashmir
merged_data.loc[merged_data['st_nm'] == 'jammu and kashmir', 'Per_Capita_Stat'] = 24.03

# 📌 Remove Ladakh from data
merged_data = merged_data[merged_data['st_nm'] != 'ladakh']

# 📌 Merge with map data
india_map1 = india_map.merge(merged_data, on="st_nm", how='left')

# 📌 Merge geometries of Jammu & Kashmir and Ladakh
jk_ladakh_geometry = unary_union(india_map1[india_map1['st_nm'].isin(['jammu and kashmir', 'ladakh'])].geometry)

# 📌 Remove Ladakh from map data and update Jammu & Kashmir
india_map1 = india_map1[india_map1['st_nm'] != 'ladakh']
india_map1.loc[india_map1['st_nm'] == 'jammu and kashmir', 'geometry'] = jk_ladakh_geometry

# 📌 Debugging check
if 'jammu and kashmir' not in india_map1['st_nm'].values:
    print("❌ ERROR: Jammu & Kashmir missing from map data!")
else:
    print("✅ Jammu & Kashmir merged successfully with value 24.03.")

# 📌 Plot Heatmap
fig, ax = plt.subplots(1, 1, figsize=(20, 15), dpi=300)

india_map1.plot(
    column="Per_Capita_Stat",
    cmap="Oranges",
    linewidth=0.8,
    edgecolor="black",
    legend=False,
    ax=ax,
    scheme='quantiles',
    k=5,
    missing_kwds={'color': 'lightgrey'}
)

# 📌 Add Color Bar
norm = mpl.colors.Normalize(
    vmin=india_map1['Per_Capita_Stat'].min(),
    vmax=india_map1['Per_Capita_Stat'].max()*0.85)


cbar = fig.colorbar(
    mpl.cm.ScalarMappable(norm=norm, cmap='YlOrRd'),
    ax=ax, orientation="vertical", shrink=0.5
)
cbar.set_label('Per Capita Interest')
offsets = {
    "jammu and kashmir": (0, -0.7),  # Move down
    "punjab": (0.6, -0.4),  # Move right-down
    "rajasthan": (-0.7, 0),  # Move Left
    "gujarat": (-0.6, -0.4),  # Move Left-Down
    "assam": (-0.7, -0.4),  # Move left-down
    "west bengal": (-0.6, -0.5),  # Move left-down
    "tamil nadu": (0, -0.7),  # Move Down
    "kerala": (-0.8, -0.8),  # Move Down More
    "andaman and nicobar islands": (0, -1.2),# Move Far Down
    "goa":(-0.9,0), #move left
    "puducherry":(1.0,0),#move right
    "andhra pradesh":(-0.4,-0.6), #move left-down
    "tripura":(-0.9,0),#move left
    "sikkim":(0,0.8), #move up
    "mizoram":(0,-2.0), #move down
    "meghalaya":(0,-0.7),
    "manipur":(1.5,-0.5),
    "nagaland":(1.5,-0.4),
    "delhi":(0.5,0),
    "chandigarh":(0.2,0.2),
    "west bengal":(0,-0.9),
    "assam":(0.3,-0.2),
    "dnh": (-0.9, 0.1),
    "dnd": (-0.9, -1.0),
    "madhya pradesh":(0,-0.3),
}

# Improve State Name & Value Visibility (Avoid Border Overlap)
for idx, row in india_map1.iterrows():
    if not row['geometry'].is_empty:
        centroid = row['geometry'].centroid
        state_name = row['st_nm']

        # Convert to uppercase only for DND & DNH, else title case
        display_name = state_name.upper() if state_name in ["DND", "DNH"] else state_name.title()

        per_capita_value = row['Per_Capita_Stat']
        per_capita_text = f"{int(per_capita_value)}" if pd.notna(per_capita_value) else ""

        # Apply Offset for every state
        state_name = row['st_nm'].strip().lower()  # Ensure consistent formatting
#offset_x, offset_y = offsets.get(state_name, (0, 0)) 
        offset_x, offset_y = offsets.get(state_name, (0, 0))
        new_x = centroid.x + offset_x
        new_y = centroid.y + offset_y

        ax.text(
            new_x, new_y,
            f"{display_name}\n{per_capita_text}",
            fontsize=8, ha='center', color='black',
            bbox=dict(facecolor='none', edgecolor='none', alpha=0.7)
        )





# 📌 Final Touches
ax.set_title("State-Wise Per Capita Interest in ChatGPT", fontsize=20, fontweight='bold')
ax.axis("off")

# 📌 Show the plot
plt.show()
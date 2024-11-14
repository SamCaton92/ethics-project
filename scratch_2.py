import tkinter as tk
from tkinter import messagebox
import galah
import pandas as pd
import math
from geopy.geocoders import Nominatim
import ssl
import certifi
import webbrowser
import sys
import tkintermapview

class AnimalLookupApp:
    def __init__(self, root):
        """Initialize the main application window and set up the UI, geolocator, and Galah configuration."""
        self.root = root
        self.root.title("Animal Lookup with Galah")
        self.root.geometry("800x600")

        # Core attributes
        self.animal_urls = {}  # Dictionary to store animal names and their URLs
        self.geolocator = self.initialize_geolocator()  # Initialize geolocation service

        # Configure Galah (API connection)
        self.configure_galah()

        # Set up the user interface
        self.setup_ui()
        

    def initialize_geolocator(self):
        """Initialize the geolocator with SSL verification using OpenStreetMap's Nominatim service."""
        try:
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            geolocator = Nominatim(
                user_agent="animal_lookup_app",
                ssl_context=ssl_context
            )
            print("Geolocator initialized successfully.")
            return geolocator
        except Exception as e:
            messagebox.showerror("Initialization Error", f"Failed to initialize geolocator: {e}")
            self.root.destroy()
            sys.exit(1)

    def configure_galah(self):
        """Configure the Galah library with the user's email for access."""
        try:
            galah.galah_config(email="samcaton92@gmail.com")
            print("Galah configured successfully.")
        except Exception as e:
            messagebox.showerror("Galah Configuration Error", f"Failed to configure Galah: {e}")
            self.root.destroy()
            sys.exit(1)

    def setup_ui(self):
        """Set up the UI layout with address input, filters, and a results list."""
        # Frames for layout organization
        address_frame = tk.LabelFrame(self.root, text="Address")
        address_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        filters_frame = tk.LabelFrame(self.root, text="Filters")
        filters_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        results_frame = tk.LabelFrame(self.root, text="Animal Names")
        results_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        mapview_frame = tk.LabelFrame(self.root, text="Map View")
        mapview_frame.grid(row=0, column=1, rowspan=3)

        # Map View
        self.mapview = tkintermapview.TkinterMapView(mapview_frame, width=425, height=500)
        self.mapview.pack()
       
        self.mapview.set_position(-27.4705, 153.0260) # Brisbane
        self.mapview.set_zoom(10)

        # Address input fields
        tk.Label(address_frame, text="Street Address:").grid(row=0, column=0, sticky="e")
        self.street_entry = tk.Entry(address_frame, width=40)
        self.street_entry.grid(row=0, column=1, padx=5)

        tk.Label(address_frame, text="City:").grid(row=1, column=0, sticky="e")
        self.city_entry = tk.Entry(address_frame, width=40)
        self.city_entry.grid(row=1, column=1, padx=5)

        tk.Label(address_frame, text="State:").grid(row=2, column=0, sticky="e")
        self.state_entry = tk.Entry(address_frame, width=40)
        self.state_entry.grid(row=2, column=1, padx=5)

        tk.Label(address_frame, text="Country:").grid(row=3, column=0, sticky="e")
        self.country_entry = tk.Entry(address_frame, width=40)
        self.country_entry.grid(row=3, column=1, padx=5)

        # Button to convert address to coordinates
        geocode_button = tk.Button(address_frame, text="Get Coordinates", command=self.geocode_address)
        geocode_button.grid(row=4, column=0, columnspan=2, pady=5)

        # Filter input fields
        tk.Label(filters_frame, text="Year Start:").grid(row=0, column=0, sticky="e")
        self.year_start_entry = tk.Entry(filters_frame, width=20)
        self.year_start_entry.grid(row=0, column=1, padx=5)

        tk.Label(filters_frame, text="Year End:").grid(row=1, column=0, sticky="e")
        self.year_end_entry = tk.Entry(filters_frame, width=20)
        self.year_end_entry.grid(row=1, column=1, padx=5)

        tk.Label(filters_frame, text="Longitude:").grid(row=2, column=0, sticky="e")
        self.longitude_entry = tk.Entry(filters_frame, width=20)
        self.longitude_entry.grid(row=2, column=1, padx=5)

        tk.Label(filters_frame, text="Latitude:").grid(row=3, column=0, sticky="e")
        self.latitude_entry = tk.Entry(filters_frame, width=20)
        self.latitude_entry.grid(row=3, column=1, padx=5)

        tk.Label(filters_frame, text="Radius (meters):").grid(row=4, column=0, sticky="e")
        self.radius_entry = tk.Entry(filters_frame, width=20)
        self.radius_entry.grid(row=4, column=1, padx=5)

        # Search button to fetch animal data
        search_button = tk.Button(filters_frame, text="Search", command=self.search_animals)
        search_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Results Listbox to display animal names with a scrollbar
        self.animal_listbox = tk.Listbox(results_frame, selectmode=tk.SINGLE)
        self.animal_listbox.grid(row=0, column=0, sticky="nsew")
        animal_scrollbar = tk.Scrollbar(results_frame, orient="vertical", command=self.animal_listbox.yview)
        animal_scrollbar.grid(row=0, column=1, sticky="ns")
        self.animal_listbox.config(yscrollcommand=animal_scrollbar.set)

        # Double-click event to open animal URL
        self.animal_listbox.bind('<Double-1>', self.on_animal_select)

        # Configure Listbox expansion within frame
        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)

    def geocode_address(self):
        """Convert an address to coordinates and display them in the UI."""
        street = self.street_entry.get()
        city = self.city_entry.get()
        state = self.state_entry.get()
        country = self.country_entry.get()
        full_address = f"{street}, {city}, {state}, {country}"

        try:
            # Use geolocator to get coordinates from address
            location = self.geolocator.geocode(full_address)
            if location:
                # Update longitude and latitude fields
                self.longitude_entry.delete(0, tk.END)
                self.latitude_entry.delete(0, tk.END)
                self.longitude_entry.insert(tk.END, location.longitude)
                self.latitude_entry.insert(tk.END, location.latitude)
                # Update Map View
                try: 
                    self.marker.delete()
                    print("Previous marker removed")
                except:
                    print("No marker to delete")          
                self.marker = self.mapview.set_position(location.latitude, location.longitude, marker=True)
                self.mapview.set_zoom(15)

                # Success popup
                messagebox.showinfo("Success", f"Address found: ({location.latitude}, {location.longitude})")
                
            else:
                messagebox.showerror("Error", "Address not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to geocode address: {e}")

    def search_animals(self):
        """Fetch animal data from Galah based on filters and display the names in the Listbox."""
        try:
            # Extract user input for search parameters
            year_start = int(self.year_start_entry.get())
            year_end = int(self.year_end_entry.get())
            longitude = float(self.longitude_entry.get())
            latitude = float(self.latitude_entry.get())
            radius = float(self.radius_entry.get())

            # Define bounding box and filters
            bbox = self.calculate_bbox(longitude, latitude, radius)
            filters = [f"year>={year_start}", f"year<={year_end}"]

            # Fetch data using galah
            atlas_output = galah.atlas_species(filters=filters, bbox=bbox)
            print("Atlas output preview:", atlas_output.head())  # For debugging

            # Columns expected in the data
            display_name_column = "Vernacular Name"  # Name to display in Listbox
            url_column = "Species"  # Column with URLs for animal details

            # Check that required columns exist and populate Listbox
            if display_name_column in atlas_output.columns and url_column in atlas_output.columns:
                # Populate dictionary with display names and URLs
                self.animal_urls = dict(zip(atlas_output[display_name_column], atlas_output[url_column]))

                # Clear Listbox and insert animal names
                self.animal_listbox.delete(0, tk.END)
                for name in self.animal_urls.keys():
                    self.animal_listbox.insert(tk.END, name)
            else:
                print("Expected columns not found in atlas_output.")
                messagebox.showinfo("No Results", "Required columns not found in data.")

        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {e}")

    def calculate_bbox(self, longitude, latitude, radius):
        """Calculate a bounding box around a point with a given radius in meters."""
        degree_to_meters = 111_000
        delta_lat = radius / degree_to_meters
        delta_lon = radius / (degree_to_meters * math.cos(math.radians(latitude)))
        return {
            "xmin": longitude - delta_lon,
            "ymin": latitude - delta_lat,
            "xmax": longitude + delta_lon,
            "ymax": latitude + delta_lat
        }

    def on_animal_select(self, event):
        """Open the URL associated with the selected animal in the default browser."""
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            animal_name = event.widget.get(index)
            url = self.animal_urls.get(animal_name)
            if url:
                webbrowser.open(url)
            else:
                messagebox.showinfo("No URL", "No URL available for this animal.")


if __name__ == "__main__":
    root = tk.Tk()
    app = AnimalLookupApp(root)
    root.mainloop()

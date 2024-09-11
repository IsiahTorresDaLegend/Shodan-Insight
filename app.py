import customtkinter as ctk
from tkinter import messagebox, simpledialog
from shodan_service import ShodanService
from key_manager import KeyManager

# Set the appearance mode and color theme
ctk.set_appearance_mode("dark") # "dark" or "light"
ctk.set_default_color_theme("blue") # Color theme

class ShodanPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Intialize the ShodanService and KeyManager Instances
        self.shodan_service = ShodanService()
        self.key_manager = KeyManager()

        # Window setup
        self.title("Shodan Insight")
        self.geometry("700x500")

        # IP Address Input Lable
        self.ip_label = ctk.CTkLabel(self, text="IP Address", font=("Arial", 12))
        self.ip_label.pack(pady=(20, 5))
        
        # IP Address Input Entry
        self.ip_address_entry = ctk.CTkEntry(self, width=300, font=("Arial", 12))
        self.ip_address_entry.pack(pady=10)

        # Search Button
        self.search_button = ctk.CTkButton(self, text="Search on Shodan", 
                                           command=self.perform_search)
        self.search_button.pack(pady=10)

        # Results Text Box
        self.results_text = ctk.CTkTextbox(self, height=500, width=600)
        self.results_text.pack(pady=(10,20))
        self.results_text.configure(state="disabled") # Disabled to prevent editiing

        # Load API key on startup
        self.load_api_key()

    def perform_search(self):
        api_key = self.key_manager.get_api_key()
        ip_address = self.ip_address_entry.get ()

        # Enable text are temporarily to insert data
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", ctk.END) # Clear previous results

        # Validate input
        if not api_key:
            messagebox.showwarning("API Key Missing",
                                    "Please configure you Shodan API key.")
            self.results_text.configure(state="disabled")
            return
        if not ip_address:
            messagebox.showwarning("IP Address Missing", 
                                    "Please provide an IP address.")
            self.results_text.configure(state="disabled")
            return
            
        # Use ShodanSevice to perform the search and display results
        result = self.shodan_service.search(ip_address, api_key)
        self.results_text.insert(ctk.END, result)
        self.results_text.configure(state="disabled") # Disable text ares to prevent editing

    def load_api_key(self):
        api_key = self.key_manager.get_api_key()
        if api_key:
            messagebox.showinfo("API Key Loaded",
                                "Your Shodan API key has been loaded successfully.")
        else:
            # If no API key is found, prompt the user to enter it 
            messagebox.showinfo("API Key Missing", "Please configure your API key.")
            self.configure_api_key()

    def configure_api_key(self):
        api_key = simpledialog.askstring("API Key",
                                        "Enter your Shodan API key:", parent=self)
        if api_key:
            self.key_manager.set_api_key(api_key)
            messagebox.showinfo("API Key", "Your Shodan API Key has been saved securely.")
        else:
            messagebox.showwarning("API Key", "No API key entered. Operation cancelled.")
        
if __name__ == "__main__":
    app = ShodanPage()
    app.mainloop()
    
                                       
import pandas as pd
from customtkinter import CTk, CTkLabel, CTkButton, CTkEntry, CTkFrame, filedialog


class ButcherRecommenderApp(CTk):
    def __init__(self):
        super().__init__()
        self.title("Butcher Recommender System")
        self.geometry("800x600")

        # UI Setup
        self.setup_ui()

    def setup_ui(self):
        frame = CTkFrame(self)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        CTkLabel(frame, text="Butcher Recommender System", font=("Arial", 24)).pack(
            pady=10
        )

        CTkButton(
            frame,
            text="Load Client History (CSV/Excel)",
            command=self.load_client_history,
        ).pack(pady=10)
        CTkButton(
            frame, text="Load Stock Data (CSV/Excel)", command=self.load_stock_data
        ).pack(pady=10)

        self.result_label = CTkLabel(frame, text="", font=("Arial", 18))
        self.result_label.pack(pady=20)

        self.recommend_button = CTkButton(
            frame,
            text="Get Recommendations",
            state="disabled",
            command=self.recommend_items,
        )
        self.recommend_button.pack(pady=10)

        self.output_frame = CTkFrame(frame)
        self.output_frame.pack(fill="both", expand=True, pady=10)

    def load_client_history(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")]
        )
        if file_path:
            try:
                self.client_history = self.load_file(file_path)
                self.result_label.configure(text="Client history loaded successfully!")
                self.enable_recommend_button()
            except Exception as e:
                self.result_label.configure(text=f"Error loading file: {e}")

    def load_stock_data(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")]
        )
        if file_path:
            try:
                self.stock_data = self.load_file(file_path)
                self.result_label.configure(text="Stock data loaded successfully!")
                self.enable_recommend_button()
            except Exception as e:
                self.result_label.configure(text=f"Error loading file: {e}")

    def load_file(self, file_path):
        if file_path.endswith(".csv"):
            return pd.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            return pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format")

    def enable_recommend_button(self):
        if hasattr(self, "client_history") and hasattr(self, "stock_data"):
            self.recommend_button.configure(state="normal")

    def recommend_items(self):
        client_items = set(self.client_history["Item"])
        stock_items = set(self.stock_data[self.stock_data["Stock"] != 0]["Item"])

        recommended_items = client_items.intersection(stock_items)

        if recommended_items:
            self.display_recommendations(recommended_items)
        else:
            self.result_label.configure(text="No matching items to recommend.")

    def display_recommendations(self, recommendations):
        for widget in self.output_frame.winfo_children():
            widget.destroy()

        CTkLabel(self.output_frame, text="Recommended Items:", font=("Arial", 18)).pack(
            pady=10
        )

        for item in recommendations:
            CTkLabel(self.output_frame, text=item, font=("Arial", 16)).pack(pady=2)


if __name__ == "__main__":
    app = ButcherRecommenderApp()
    app.mainloop()

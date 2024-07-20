# Global Statistics Dashboard

The Global Statistics Dashboard is a comprehensive tool designed to provide insights into various global statistics. This project includes data processing scripts, a web application interface, and modular components for loading and visualizing data.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Libraries Used](#libraries-used)
- [License](#license)
- [Contributing](#contributing)

## <i>Installation</i>

1. Clone the repository:
   ```sh
   git clone https://github.com/UznetDev/Global-Internet-users.git
   ```
2. Navigate to the project directory:
   ```sh
   cd Global-Internet-users
   ```
3. Create a virtual environment:
   ```sh
   python -m venv env
   ```
4. Activate the virtual environment:
   - On Windows:
     ```sh
     env\Scripts\activate
     ```
   - On macOS and Linux:
     ```sh
     source env/bin/activate
     ```
5. Install the necessary libraries:
   ```sh
   pip install -r requirements.txt
   ```
## Usage

To run the dashboard, use the following command:
```bash
streamlit run 🏠_Home.py
```

This will start the application, and you can view it in your web browser by navigating to `http://localhost:5000` (or the specified port).

## Project Structure

- `.gitignore`: Specifies files and directories to be ignored by git.
- `build_data.ipynb`: Jupyter Notebook for building, cleaning and processing the dataset.
- `dataset/`: Directory containing the dataset files used for the dashboard.
- `function.py`: Contains functions used across the project.
- `🏠_Home.py`: The main script to run the web application.
- `loader.py`: Script responsible for loading data into the application.
- `pages/`: Directory containing the different pages of the web application.
    - **1_🗺️Map.py**: This module contains the code for displaying a global map with various statistical overlays. It visualizes geographical data and provides interactive map features.
    - **2_ 📊Statistics_by_country.py**: This module provides statistical data breakdowns by country. Users can select a country and view detailed statistics relevant to that country.
    - **3_🎯_Future_Product.py**: This module is designed for future product implementations. It serves as a placeholder for features that are planned for future releases.
    - **__init__.py**: This file indicates that the `pages` directory is a Python package.


### Detailed Breakdown

- **.gitignore**: Configuration file to specify untracked files that Git should ignore.
- **build_data.ipynb**: Jupyter Notebook for data preprocessing. This includes steps to clean, transform, and prepare data for visualization.
- **dataset/**: This folder holds raw and processed data files necessary for generating statistics.
- **function.py**: This module contains reusable functions that are utilized in various parts of the project to ensure modularity and code reuse.
- **🏠_Home.py**: The entry point for the web application. Running this script launches the dashboard.
- **loader.py**: Handles data loading operations. This script ensures that the data from the `dataset` directory is correctly loaded and ready for use in the application.
- **pages/**: Contains different page modules for the web application. Each page is a separate component/module that can be accessed through the dashboard interface.

## Libraries Used

The following libraries are used in this project:

- **pandas**: For data manipulation and analysis.
- **numpy**: For numerical operations.
- **plotly**: For creating interactive visualizations.
- **streamlit**: For building the web application.
- **Matplotlib**: For making Dashboard.
- **jupyter**: For interactive computing and developing the `build_data.ipynb` notebook.

These libraries are listed in the `requirements.txt` file and can be installed using the installation instructions provided above.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any changes.

1. **Fork the Repository**:
    Click on the `Fork` button at the top right corner of this page to create a copy of this repository under your GitHub account.

2. **Clone the Forked Repository**:
    ```bash
    git clone https://github.com/YOUR_USERNAME/Global-Statistics-Dashboard.git
    cd Global-Statistics-Dashboard
    ```

3. **Create a New Branch**:
    ```bash
    git checkout -b feature/YourFeatureName
    ```

4. **Commit Your Changes**:
    ```bash
    git add .
    git commit -m 'Add some feature'
    ```

5. **Push to the Branch**:
    ```bash
    git push origin feature/YourFeatureName
    ```

6. **Create a Pull Request**:
    Open a pull request to the original repository.

## <i>Contact</i>

If you have any questions or suggestions, please contact:
- Email: uznetdev@example.com
- GitHub Issues: [Issues section](https://github.com/UznetDev/Global-Statistics-Dashboard/issues)
- GitHub Profile: [UznetDev](https://github.com/UznetDev/)
- Telegram: [UZNet_Dev](https://t.me/UZNet_Dev)
- Linkedin: [Abdurahmon Niyozaliev](https://www.linkedin.com/in/abdurakhmon-niyozaliyev-%F0%9F%87%B5%F0%9F%87%B8-66545222a/)


### <i>Thank you for your interest in the project!</i>

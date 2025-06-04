from shiny import App, ui, render, reactive
import importlib.util
import sys
import os

# Try to import the private package
package_name = "tiny_private_utils"
package_available = False
package_version = "unknown"

try:
    # Attempt to import the package
    spec = importlib.util.find_spec(package_name)
    if spec is not None:
        tiny_private_utils = importlib.import_module(package_name)
        package_available = True
        
        # Try to get the version
        try:
            package_version = tiny_private_utils.__version__
        except AttributeError:
            package_version = "version not specified"
except ImportError:
    pass

app_ui = ui.page_sidebar(
    ui.panel_title("Private Package Integration Demo"),
    
    ui.sidebar(
        ui.h4("Package Controls"),
        ui.input_text("name", "Enter your name:", value="User"),
        ui.input_select(
            "text_style", 
            "Text style:", 
            {"bold": "Bold", "italic": "Italic", "code": "Code"}
        ),
        ui.input_text_area(
            "numbers",
            "Enter numbers (comma separated):",
            value="1, 2, 3, 4, 5",
            height="100px"
        ),
        ui.input_action_button("calculate", "Calculate Stats"),
    ),
    
    ui.card(
        ui.h3("Package Status"),
        ui.output_text("package_status"),
        ui.output_text("package_info"),
    ),
    
    ui.card(
        ui.h3("Greeting Demo"),
        ui.output_text("greeting_output"),
        ui.h4("Styled Text Demo"),
        ui.output_text("styled_text"),
    ),
    
    ui.card(
        ui.h3("Statistics Demo"),
        ui.output_text("stats_output"),
    )
)

def server(input, output, session):
    
    @render.text
    def package_status():
        if package_available:
            return f"✅ Private package '{package_name}' is successfully installed!"
        else:
            return f"❌ Private package '{package_name}' is not available. Check installation."
    
    @render.text
    def package_info():
        if package_available:
            # List functions that don't start with underscore (public functions)
            funcs = [attr for attr in dir(tiny_private_utils) 
                    if callable(getattr(tiny_private_utils, attr)) and not attr.startswith('_')]
            funcs_str = ", ".join(funcs)
            
            return f"Package: {package_name}\nVersion: {package_version}\nAvailable functions: {funcs_str}"
        else:
            return "Package information not available"
    
    @render.text
    def greeting_output():
        name = input.name()
        if package_available:
            try:
                return tiny_private_utils.generate_greeting(name)
            except AttributeError:
                return f"Hello, {name}! (function generate_greeting not found in package)"
        else:
            return f"Hello, {name}! (Default greeting since package is not available)"
    
    @render.text
    def styled_text():
        name = input.name()
        style = input.text_style()
        text = f"Hello, {name}!"
        
        if package_available:
            try:
                return tiny_private_utils.format_text(text, style)
            except AttributeError:
                return f"{text} (function format_text not found in package)"
        else:
            styles = {
                "bold": f"*{text}*",
                "italic": f"_{text}_",
                "code": f"`{text}`"
            }
            return f"{styles.get(style, text)} (Default styling since package is not available)"
    
    stats = reactive.value(None)
    
    @reactive.effect
    @reactive.event(input.calculate)
    def _():
        try:
            # Parse the numbers
            nums_str = input.numbers().split(',')
            numbers = [float(num.strip()) for num in nums_str if num.strip()]
            
            if package_available and hasattr(tiny_private_utils, 'calculate_stats'):
                result = tiny_private_utils.calculate_stats(numbers)
            else:
                # Fallback implementation
                result = {
                    "count": len(numbers),
                    "sum": sum(numbers),
                    "avg": sum(numbers) / len(numbers) if numbers else 0,
                    "min": min(numbers) if numbers else None,
                    "max": max(numbers) if numbers else None
                }
            stats.set(result)
        except Exception as e:
            stats.set({"error": str(e)})
    
    @render.text
    def stats_output():
        if stats() is None:
            return "Enter numbers and click 'Calculate Stats'"
        
        if "error" in stats():
            return f"Error: {stats()['error']}"
        
        stats_dict = stats()
        result = "Statistics:\n"
        for key, value in stats_dict.items():
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                result += f"- {key}: {value:.2f}\n"
            else:
                result += f"- {key}: {value}\n"
                
        source = "using private package" if package_available else "using fallback implementation"
        return result + f"\n(Calculated {source})"

app = App(app_ui, server)

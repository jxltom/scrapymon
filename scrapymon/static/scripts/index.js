// Importing jQuery which is required by FlatUI
import "jquery";

// Importing FlatUI via imports-loader since FlatUI relys on $ being window
require("imports-loader?this=>window!../libs/flatui/app/scripts/flat-ui");

// Importing scss for Bootstrap which is required by FlatUI
import "../styles/index.scss";
// Importing scss for FlatUI
import "../libs/flatui/app/styles/flat-ui.scss";

// Importing custom js
import "./app"

const path = require("path");
const webpack = require("webpack");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const ManifestRevisionPlugin = require("manifest-revision-webpack-plugin");
const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  entry: "./scrapymon/static/scripts/index.js",
  output: {
    path: path.resolve(__dirname, "scrapymon/static/assets"),
    filename: "[name].[hash].js",
    chunkFilename: "[name].[hash].js",
    publicPath: "/static/assets/"
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [MiniCssExtractPlugin.loader, "css-loader"]
      },
      {
        test: /\.(scss)$/,
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: "css-loader" // translates CSS into CommonJS modules
          },
          {
            loader: "postcss-loader", // Run post css actions
            options: {
              plugins: function() {
                // post css plugins, can be exported to postcss.config.js
                return [require("precss"), require("autoprefixer")];
              }
            }
          },
          {
            loader: "sass-loader" // compiles Sass to CSS
          }
        ]
      },
      {
        test: /\.(eot|otf|png|svg|jpg|ttf|woff|woff2)(\?v=[0-9.]+)?$/,
        loader: "file-loader?name=[name].[hash].[ext]"
      }
    ]
  },
  plugins: [
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
      "window.$": "jquery",
      "window.jQuery": "jquery"
    }),
    new MiniCssExtractPlugin({
      filename: "[name].[hash].css",
      chunkFilename: "[id].[hash].css"
    }),
    new ManifestRevisionPlugin("./webpack-manifest.json", {
      rootAssetPath: "./scrapymon/static",
      ignorePaths: ["scrapymon/static/libs", "scrapymon/static/assets"]
    }),
    new BundleTracker({
      path: __dirname,
      filename: "./webpack-stats.json"
    })
  ]
};

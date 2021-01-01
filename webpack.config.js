const path = require("path");

const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const MomentLocalesPlugin = require("moment-locales-webpack-plugin");

module.exports = {
  entry: {
    index: "./src/index.js",
    runningMap: "./src/running_map.js",
    daylight: "./src/daylight.js",
  },
  output: {
    filename: "[name].bundle.js",
    path: path.resolve(__dirname, "site/dist/"),
  },
  devtool: "eval-cheap-source-map",
  plugins: [new MiniCssExtractPlugin(), new MomentLocalesPlugin()],
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
            options: {
              publicPath: "",
            },
          },
          {
            loader: "css-loader",
          },
        ],
      },
      {
        test: /\.less$/,
        use: [MiniCssExtractPlugin.loader, "css-loader", "less-loader"],
      },
      {
        test: /\.png$/,
        use: ["file-loader"],
      },
    ],
  },
  optimization: {
    minimize: true,
    minimizer: [new CssMinimizerPlugin()],
  },
};

const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');
const TerserPlugin = require('terser-webpack-plugin');

module.exports = {
  plugins: [new MiniCssExtractPlugin()],
  entry: {
    index: './src/index.js',
    runningMap: './src/running_map.js',
    daylight: './src/daylight.js',
  },
  output: {
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, 'site/dist/'),
  },
  module: {
    rules: [
      {
	test: /\.css$/,
	use: [
	  {
            loader: MiniCssExtractPlugin.loader,
            options: {
              publicPath: ''
            }
          },
	  {
            loader: "css-loader"
          }
	],
      },
      {
        test: /\.less$/,
        use: [
	  MiniCssExtractPlugin.loader,
	  'css-loader',
	  'less-loader'
	],
      },
      {
        test: /\.png$/,
        use: [
          'file-loader'
        ]
      },
    ],
  },
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin(),
      new CssMinimizerPlugin(),
    ],
  },
};

const webpack = require('webpack'); // to access built-in plugins
const path = require('path');

module.exports = {
  entry: [
    // https://github.com/facebook/react/issues/8379
    'babel-polyfill', // Load this first
    //'react-hot-loader/patch', // This package already requires/loads react (but not react-dom). It must be loaded after babel-polyfill to ensure both react and react-dom use the same Symbol.
    'react', // Include this to enforce order
    'react-dom', // Include this to enforce order
    './js/dashboard.js' // Path to your app's entry file
  ],
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, '../backend/hqlib/app/dist'),
    publicPath: 'dist/'
  },
  resolve: {
    modules: [
      path.resolve('./js'),
      path.resolve('./node_modules')
    ]
  },
  plugins: [
    new webpack.ProvidePlugin({
      jQuery: 'jquery',
      $: 'jquery',
      jquery: 'jquery'
    }),
    new webpack.optimize.UglifyJsPlugin()
  ],
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        use: 'babel-loader'
      },
      {
        test: /\.css$/,
        use: [ 'style-loader', 'css-loader' ]
      },
      {
	test: /\.woff(\?v=\d+\.\d+\.\d+)?$/,
	use: [{
          loader: 'file-loader',
          options: {
            limit: 10000,
            mimetype: 'application/font-woff'
          }
        }]
      },
      {
        test: /\.woff2(\?v=\d+\.\d+\.\d+)?$/,
        use: [{
          loader: 'file-loader',
          options: {
            limit: 10000,
            mimetype: 'application/font-woff2'
          }
        }]
      },
      {
        test: /\.[ot]tf(\?v=\d+\.\d+\.\d+)?$/,
        use: [{
          loader: 'file-loader',
          options: {
            limit: 10000,
            mimetype: 'application/octet-stream'
          }
        }]
      },
      {
        test: /\.eot(\?v=\d+\.\d+\.\d+)?$/,
        loader: "file-loader"
      },
      {
        test: /\.svg(\?v=\d+\.\d+\.\d+)?$/,
        use: [{
          loader: 'file-loader',
          options: {
            limit: 10000,
            mimetype: 'image/svg+xml'
          }
        }]
      }
    ]
  }
};

var path = require('path');
var webpack = require('webpack');

module.exports = {
  entry: [
    './src/app.tsx'
    ],
  output: {
    path: path.join(__dirname, 'dist'),
    filename: 'bundle.js',
    publicPath: '/static/'
  },
  resolve: {
    // Add `.ts` and `.tsx` as a resolvable extension.
    extensions: ['', '.webpack.js', '.web.js', '.ts', '.tsx', '.js']
  },
  module: {
    loaders: [
      // all files with a `.ts` or `.tsx` extension will be handled by `ts-loader`
    { test: /\.tsx?$/, loader: 'ts-loader' },
    { test: /\.less$/, loader: 'style!css!less' }
    ],
      preLoaders: [
        // All output '.js' files will have any sourcemaps re-processed by 'source-map-loader'.
      { test: /\.js$/, loader: 'source-map-loader' }
    ]
  },
}


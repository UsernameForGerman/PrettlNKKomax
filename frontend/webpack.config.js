const HtmlWebPackPlugin = require( 'html-webpack-plugin' );
const Dotenv = require('dotenv-webpack');
const path = require( 'path' );
module.exports = {
    context: __dirname,
    entry: './src/index.js',
    output: {
        path: path.resolve( __dirname, 'static/komax_app' ),
        filename: 'main.js',
        publicPath: '/',
    },
    devServer: {
        historyApiFallback: true,
        host : "localhost",
        port : 3000
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                use: 'babel-loader',
            },
            {
                test: /\.css$/,
                use: [
                    'style-loader',
                    {
                        loader: 'css-loader',
                        options: {
                            modules: {
                                auto: true
                            }
                        }
                    }
                ]
            },
            {
                test: /\.(png|j?g|svg|gif|jpeg|jpg)?$/,
                use: 'file-loader'
            },
            {
                test: /\.less$/,
                loader: 'less-loader',
                options: { javascriptEnabled: true }
            },
            {
                test: /\.(mp4)?$/,
                use: 'file-loader'
            },
            {
                test: /\.(otf|eot|woff|woff2|svg|ttf)([\?]?.*)$/,
                use: [
                    {
                        loader: 'file-loader?name=assets/[name].[ext]',
                    }
                ]
            },
            {
                test: /\.xlsx$/,
                loader: "webpack-xlsx-loader"
            }
        ]
    },
    plugins: [
        new HtmlWebPackPlugin({
            template: path.resolve( __dirname, 'public/index.html' ),
            filename: 'index.html'
        }),
        new Dotenv({
          path: path.resolve( __dirname, '.env' ), // Path to .env file (this is the default)
          safe: false // load .env.example (defaults to "false" which does not use dotenv-safe)
        })
    ]
};
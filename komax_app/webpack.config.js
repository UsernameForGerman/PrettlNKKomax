const HtmlWebPackPlugin = require( 'html-webpack-plugin' );
const path = require( 'path' );
module.exports = {
    context: __dirname,
    entry: './src/index.js',
    output: {
        path: path.resolve( __dirname, 'static/komax_app' ),
        filename: 'main.js',
        publicPath: 'static/komax_app/',
    },
    devServer: {
        historyApiFallback: true,
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
                            importLoaders: 1,
                            modules: true
                        }
                    }
                ]
            },
            {
                test: /\.(png|j?g|svg|gif|jpeg|jpg)?$/,
                use: 'file-loader'
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
            }
        ]
    },
    plugins: [
        new HtmlWebPackPlugin({
            template: path.resolve( __dirname, 'public/index.html' ),
            filename: 'index.html'
        })
    ]
};
const path = require("path");

module.exports = {
    
  publicPath: process.env.VUE_APP_STATIC_URL,
  outputDir: path.resolve(__dirname, "../static", "mtpinfoshare"),
  indexPath: path.resolve(__dirname, "../templates/", "mtpinfoshare", "index.html"),
  //devServer:{proxy:'http://192.100.200.23:8033'},
  
};


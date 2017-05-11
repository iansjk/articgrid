module.exports = function(grunt) {
    require('load-grunt-tasks')(grunt);

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        bowercopy: {
            scripts: {
                options: {
                    'destPrefix': 'static/vendor/'
                },
                files: {
                    'jquery.min.js': 'jquery/dist/jquery.min.js',
                    'bootstrap.min.js': 'bootstrap/dist/js/bootstrap.min.js',
                    'jquery.dataTables.min.js': 'datatables.net/js/jquery.dataTables.min.js'
                }
            },
            style: {
                options: {
                    destPrefix: 'static/vendor/'
                },
                files: {
                    'bootstrap.min.css': 'bootstrap/dist/css/bootstrap.min.css'
                }
            }
        },
        replace: {
            twbs_mapfile: {
                options: {
                    patterns: [
                        {
                            match: '/*# sourceMappingURL=bootstrap.min.css.map */',
                            replacement: '',
                        }
                    ],
                    usePrefix: false
                },
                files: {
                    'static/vendor/bootstrap.min.css': 'bower_components/bootstrap/dist/css/bootstrap.min.css'
                }
            }
        }
    });
    grunt.registerTask('default', ['bowercopy', 'replace']);
};


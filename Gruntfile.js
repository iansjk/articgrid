module.exports = function(grunt) {
    require('load-grunt-tasks')(grunt);

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        jshint: {
            options: {
                jshintrc: '.jshintrc'
            },
            all: ['static/*.js']
        },
        bowercopy: {
            scripts: {
                options: {
                    'destPrefix': 'static/vendor/'
                },
                files: {
                    'jquery.min.js': 'jquery/dist/jquery.min.js',
                    'bootstrap.min.js': 'bootstrap/dist/js/bootstrap.min.js',
                    'jquery.imgcheckbox.js': 'imgcheckbox/jquery.imgcheckbox.js',
                    'tether.min.js': 'tether/dist/js/tether.min.js',
                    'holder.min.js': 'holderjs/holder.min.js',
                    'jquery.dataTables.min.js': 'datatables.net/js/jquery.dataTables.min.js',
                    'dataTables.select.min.js': 'datatables.net-select/js/dataTables.select.min.js',
                }
            },
            style: {
                options: {
                    destPrefix: 'static/vendor/'
                },
                files: {
                    'bootstrap.min.css': 'bootstrap/dist/css/bootstrap.min.css'
                }
            },
            fontawesome: {
                options: {
                    destPrefix: 'static/vendor'
                },
                files: {
                    'fontawesome/css': 'components-font-awesome/css',
                    'fontawesome/fonts': 'components-font-awesome/fonts'
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
            },
            datatables_cache: {
                options: {
                    patterns: [
                        {
                            match: 'cache:!1',
                            replacement: 'cache:!0'
                        }
                    ],
                    usePrefix: false
                },
                files: {
                    'static/vendor/jquery.dataTables.min.js': 'bower_components/datatables.net/js/jquery.dataTables.min.js'
                }
            }
        }
    });
    grunt.registerTask('default', ['bowercopy', 'replace']);
};


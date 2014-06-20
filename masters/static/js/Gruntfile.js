module.exports = function(grunt) {
  var TESTING_PORT = 9001;

  grunt.initConfig({
    shell: {
      'mocha-phantomjs': {
        command: 'mocha-phantomjs -R dot tests/index.html',
        options: {
          stdout: true,
          stderr: true
        }
      },

      'ci': {
        command: 'mocha-phantomjs -R spec http://localhost:' + TESTING_PORT +'/tests/index.html',
        options: {
          stdout: true,
          stderr: true
        }
      }
    },
    mocha: {
      test: {
        // src: ['tests/**/*.html'],
        // src: ['tests/index.html'],
        options: {
          run: true,
          urls: ["http://localhost:9001/tests/index.html"]
        }
      },
    },
    connect: {
        test: {
            options: {
                port: TESTING_PORT,
                base: '.'
            }
        }
    },
    watch: {
      jsFiles: {
        files: ['**/*.js', '!app.min.js','**/*.html'],
        // tasks: ['connect:test', 'shell:ci']
        tasks: ['requirejs:compile']
      }
    },
    requirejs: {
        compile: {
            options: {
                mainConfigFile: "app/app.js",
                out: "app.min.js",
                findNestedDependencies: true,
                optimize: "uglify",
                include: "app.js",
                logLevel: 0,
                inlineText: true
          }
        }
      }
  });

  grunt.loadNpmTasks('grunt-contrib-connect');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-mocha');
  grunt.loadNpmTasks('grunt-shell');
  grunt.loadNpmTasks('grunt-contrib-requirejs');

  grunt.registerTask('test', ['connect:test', 'shell:ci']);
};

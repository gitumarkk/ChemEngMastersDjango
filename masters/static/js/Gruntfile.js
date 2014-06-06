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
        files: ['**/*.js'],
        tasks: ['connect:test', 'shell:ci']
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-connect');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-mocha');
  grunt.loadNpmTasks('grunt-shell');

  grunt.registerTask('test', ['connect:test', 'shell:ci']);
};

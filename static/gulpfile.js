var gulp = require('gulp'),
    imagemin = require('gulp-imagemin'),
    uglify = require('gulp-uglify'),
    minifyCss = require('gulp-minify-css'),
    plumber = require('gulp-plumber'),
    autoprefixer = require('gulp-autoprefixer'); // for error handling

// default
gulp.task('default', function() {

});

// crossbrowser autoprefix
gulp.task('autoprefix', function(){
    return gulp.src('css/*.css')
        .pipe(autoprefixer({
            browsers: ['last 10 versions'],
            cascade: false
        }))
        .pipe(gulp.dest('css'));
});

// watch changes of files
gulp.task('watch', function() {
    gulp.watch('css/*.css', ['minify-css']);
});

// compress images
gulp.task('image', function() {
    gulp.src('images/*')
        .pipe(imagemin())
        .pipe (gulp.dest('images/compression'));
});

// compress js
gulp.task('compress', function() {
  return gulp.src('js/*.js')
    .pipe(uglify())
    .pipe(gulp.dest('js/minified'));
});

// compress css
gulp.task('minify-css', function() {
  return gulp.src('css/*.css')
    .pipe(plumber())
    .pipe(minifyCss({compatibility: 'ie8'}))
    .pipe(gulp.dest('css/minified'));
});

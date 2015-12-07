var gulp = require('gulp'),
    imagemin = require('gulp-imagemin'),
    uglify = require('gulp-uglify'),
    minifyCss = require('gulp-minify-css'),
    plumber = require('gulp-plumber'), // for error handling
    autoprefixer = require('gulp-autoprefixer'),
<<<<<<< HEAD
    sass = require('gulp-sass'),
    livereload = require('gulp-livereload');
=======
    sass = require('gulp-sass');
>>>>>>> 94c894deddfa06d7f5a77a54b7049c9a1c72c787

// default
gulp.task('default', function() {

});

// crossbrowser autoprefix
gulp.task('autoprefix', function(){
    return gulp.src('css/*.css')
        .pipe(autoprefixer({
            browsers: ['last 5 versions'],
            cascade: false
        }))
        .pipe(gulp.dest('css'));
});


// watch changes of files
gulp.task('html', function() {
    return gulp.src('partials/*.html')
        .pipe(gulp.dest(''))
        .pipe(livereload());
});


// watch changes of files
gulp.task('watch', function() {
<<<<<<< HEAD
    livereload.listen();
    gulp.watch('css/*.css', ['minify-css', 'sass']);
    gulp.watch('partials/*.html', ['html']);
=======
    gulp.watch('css/*.css', ['minify-css', 'sass']);
>>>>>>> 94c894deddfa06d7f5a77a54b7049c9a1c72c787
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
    .pipe(gulp.dest('css/minified'))
    .pipe(livereload());
});


// SCSS
gulp.task('sass', function () {
  gulp.src('sass/*.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(gulp.dest('css/sass'));
});
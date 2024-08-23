angular.module('attendanceApp', [])
    .controller('MainController', ['$scope', '$http', function($scope, $http) {
        $scope.showOptions = true;
        $scope.showAttendance = false;
        $scope.attendancePredictions = [];
        $scope.showClassAttendance = false;
        $scope.showIndividualAttendance = false;

        $scope.toggleOptions = function() {
            $scope.showOptions = !$scope.showOptions;
            $scope.showAttendance = !$scope.showAttendance;
        };

        $scope.takeAttendance = function() {
            if ($scope.file) {
                var formData = new FormData();
                formData.append('file', $scope.file);
                $http.post('/attendance', formData, {
                    transformRequest: angular.identity,
                    headers: { 'Content-Type': undefined }
                }).then(function(response) {
                    $scope.attendancePredictions = response.data.predictedNames;
                });
            } else if ($scope.cameraNum) {
                // Implement camera capture logic
            }
        };

        $scope.getClassAttendance = function() {
            $http.get('/class_attendance').then(function(response) {
                // Handle response to display class attendance
                $scope.showClassAttendance = true;
            });
        };

        $scope.checkIndividualAttendance = function() {
            $scope.showIndividualAttendance = true;
        };

        $scope.checkAttendance = function() {
            if ($scope.studentName) {
                $http.post('/individual_attendance', { studentName: $scope.studentName }).then(function(response) {
                    $scope.individualAttendance = response.data.attendancePercentage;
                });
            }
        };
    }]);

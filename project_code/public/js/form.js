var livePainting = angular.module('livePainting', ['colorpicker.module']);

function mainController($scope, $http) {
	$scope.formData = {};

	$http.get('/api/options')
		.success(function(data) {
			$scope.options = data;
            $scope.currentOption = $scope.options[1].type;
		})
		.error(function(data) {
			console.log('Error: ' + data);
		});

	$scope.sendOptions = function() {
		$http.post('/api/currentoption', $scope.selection)
			.success(function(data) {
			})
			.error(function(data) {
				console.log('Error: ' + data);
			});
	};
}

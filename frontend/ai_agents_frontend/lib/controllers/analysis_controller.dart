import 'package:get/get.dart';
import '../services/api_service.dart';

class AnalysisController extends GetxController {
  final ApiService _apiService = ApiService();
  final RxMap<String, dynamic> analysisResults = <String, dynamic>{}.obs;
  final RxBool isLoading = false.obs;
  final RxString errorMessage = ''.obs;

  Future<void> performAnalysis(String query) async {
    if (query.trim().isEmpty) {
      Get.snackbar('Errore', 'Inserisci una query valida');
      return;
    }

    isLoading.value = true;
    errorMessage.value = '';
    analysisResults.clear();

    try {
      print('Starting analysis for query: $query'); // Debug

      final results = await _apiService.analyze(query);

      print('Analysis results received: $results'); // Debug

      analysisResults.value = results;

      Get.toNamed('/analysis-results', arguments: {'query': query});
    } catch (e) {
      print('Analysis error: $e'); // Debug
      errorMessage.value = e.toString();
      Get.snackbar(
        'Errore',
        'Errore durante l\'analisi: ${e.toString()}',
        duration: const Duration(seconds: 5),
      );
    } finally {
      isLoading.value = false;
    }
  }
}

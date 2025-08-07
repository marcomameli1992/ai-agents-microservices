import 'package:get/get.dart';
import '../models/search_result.dart';
import '../services/api_service.dart';

class AppSearchController extends GetxController {
  final ApiService _apiService = ApiService();
  final RxList<SearchResult> searchResults = <SearchResult>[].obs;
  final RxBool isLoading = false.obs;
  final RxString errorMessage = ''.obs;

  Future<void> performSearch(String query) async {
    if (query.trim().isEmpty) return;

    isLoading.value = true;
    errorMessage.value = '';

    try {
      final results = await _apiService.search(query);
      searchResults.value = results;
      Get.toNamed('/search-results', arguments: {'query': query});
    } catch (e) {
      errorMessage.value = e.toString();
      Get.snackbar('Errore', e.toString());
    } finally {
      isLoading.value = false;
    }
  }
}

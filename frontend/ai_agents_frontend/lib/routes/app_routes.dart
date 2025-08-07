import 'package:get/get.dart';
import '../views/home_page.dart';
import '../views/search_results_page.dart';
import '../views/analysis_results_page.dart';

class AppRoutes {
  static const String home = '/';
  static const String searchResults = '/search-results';
  static const String analysisResults = '/analysis-results';

  static List<GetPage> routes = [
    GetPage(name: home, page: () => const HomePage()),
    GetPage(name: searchResults, page: () => const SearchResultsPage()),
    GetPage(name: analysisResults, page: () => const AnalysisResultsPage()),
  ];
}

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:url_launcher/url_launcher.dart';
import '../controllers/analysis_controller.dart';

class AnalysisResultsPage extends StatelessWidget {
  const AnalysisResultsPage({super.key});

  @override
  Widget build(BuildContext context) {
    final analysisController = Get.find<AnalysisController>();
    final String query = Get.arguments?['query'] ?? '';

    return Scaffold(
      appBar: AppBar(
        title: Text('Analisi per: "$query"'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Obx(() {
        if (analysisController.isLoading.value) {
          return const Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                CircularProgressIndicator(),
                SizedBox(height: 16),
                Text('Analizzando i contenuti...'),
              ],
            ),
          );
        }

        final results = analysisController.analysisResults;

        // Debug: stampa i risultati
        print('Analysis results: $results');

        if (results.isEmpty) {
          return const Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.info_outline, size: 64, color: Colors.grey),
                SizedBox(height: 16),
                Text(
                  'Nessun risultato di analisi disponibile',
                  style: TextStyle(fontSize: 18),
                ),
              ],
            ),
          );
        }

        // Gestisci diversi formati di risposta
        final searchResults = _getSearchResults(results);
        final analysis = _getAnalysis(results);

        print('Search results count: ${searchResults.length}');
        print('Analysis count: ${analysis.length}');

        if (searchResults.isEmpty) {
          return const Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.search_off, size: 64, color: Colors.grey),
                SizedBox(height: 16),
                Text(
                  'Nessun risultato di ricerca trovato',
                  style: TextStyle(fontSize: 18),
                ),
              ],
            ),
          );
        }

        return ListView.builder(
          padding: const EdgeInsets.all(16),
          itemCount: searchResults.length,
          itemBuilder: (context, index) {
            final searchResult = searchResults[index];
            final analysisData = index < analysis.length ? analysis[index] : {};

            return Card(
              margin: const EdgeInsets.only(bottom: 16),
              elevation: 4,
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Titolo e URL
                    GestureDetector(
                      onTap: () async {
                        final url = _getUrl(searchResult);
                        if (url.isNotEmpty) {
                          final uri = Uri.parse(url);
                          if (await canLaunchUrl(uri)) {
                            await launchUrl(uri);
                          }
                        }
                      },
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            _getTitle(searchResult),
                            style: const TextStyle(
                              color: Colors.blue,
                              fontWeight: FontWeight.bold,
                              fontSize: 16,
                              decoration: TextDecoration.underline,
                            ),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            _getUrl(searchResult),
                            style: const TextStyle(
                              color: Colors.green,
                              fontSize: 12,
                            ),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            _getSnippet(searchResult),
                            style: const TextStyle(fontSize: 14),
                          ),
                        ],
                      ),
                    ),

                    const Divider(),

                    // Dati di analisi
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: Colors.grey[100],
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            '🔍 Dati Estratti:',
                            style: TextStyle(
                              fontWeight: FontWeight.bold,
                              fontSize: 16,
                            ),
                          ),
                          const SizedBox(height: 8),
                          if (analysisData.isNotEmpty)
                            ...analysisData.entries.map((entry) {
                              return Padding(
                                padding: const EdgeInsets.only(bottom: 6),
                                child: Row(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      '${entry.key}: ',
                                      style: const TextStyle(
                                        fontSize: 14,
                                        fontWeight: FontWeight.w600,
                                      ),
                                    ),
                                    Expanded(
                                      child: Text(
                                        '${entry.value}',
                                        style: const TextStyle(fontSize: 14),
                                      ),
                                    ),
                                  ],
                                ),
                              );
                            }).toList()
                          else
                            const Text(
                              'Nessun dato estratto disponibile per questo risultato',
                              style: TextStyle(
                                fontSize: 14,
                                fontStyle: FontStyle.italic,
                                color: Colors.grey,
                              ),
                            ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            );
          },
        );
      }),
    );
  }

  List<dynamic> _getSearchResults(Map<String, dynamic> results) {
    // Prova diversi formati possibili
    if (results.containsKey('search_results')) {
      final searchResults = results['search_results'];
      if (searchResults is List) return searchResults;
    }

    if (results.containsKey('results')) {
      final searchResults = results['results'];
      if (searchResults is List) return searchResults;
    }

    // Se la risposta è direttamente una lista
    if (results.containsKey('query') && results.length > 1) {
      // Potrebbe essere un oggetto con query e altri dati
      return results.entries
          .where((entry) => entry.key != 'query')
          .map((entry) => entry.value)
          .where((value) => value is Map)
          .toList();
    }

    return [];
  }

  List<dynamic> _getAnalysis(Map<String, dynamic> results) {
    if (results.containsKey('analysis')) {
      final analysis = results['analysis'];
      if (analysis is List) return analysis;
      if (analysis is Map) return [analysis];
    }

    return [];
  }

  String _getTitle(dynamic searchResult) {
    if (searchResult is Map<String, dynamic>) {
      return searchResult['title']?.toString() ?? 'Titolo non disponibile';
    }
    return 'Titolo non disponibile';
  }

  String _getUrl(dynamic searchResult) {
    if (searchResult is Map<String, dynamic>) {
      return searchResult['url']?.toString() ??
          searchResult['link']?.toString() ??
          '';
    }
    return '';
  }

  String _getSnippet(dynamic searchResult) {
    if (searchResult is Map<String, dynamic>) {
      return searchResult['snippet']?.toString() ??
          searchResult['body']?.toString() ??
          searchResult['description']?.toString() ??
          'Nessuna descrizione disponibile';
    }
    return 'Nessuna descrizione disponibile';
  }
}

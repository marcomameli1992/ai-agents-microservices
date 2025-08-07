import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:url_launcher/url_launcher.dart';
import '../controllers/search_controller.dart';

class SearchResultsPage extends StatelessWidget {
  const SearchResultsPage({super.key});

  @override
  Widget build(BuildContext context) {
    final searchController = Get.find<AppSearchController>();
    final String query = Get.arguments['query'] ?? '';

    return Scaffold(
      appBar: AppBar(
        title: Text('Risultati per: "$query"'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Obx(() {
        if (searchController.isLoading.value) {
          return const Center(child: CircularProgressIndicator());
        }

        if (searchController.searchResults.isEmpty) {
          return const Center(child: Text('Nessun risultato trovato'));
        }

        return ListView.builder(
          padding: const EdgeInsets.all(16),
          itemCount: searchController.searchResults.length,
          itemBuilder: (context, index) {
            final result = searchController.searchResults[index];
            return Card(
              margin: const EdgeInsets.only(bottom: 16),
              child: ListTile(
                title: Text(
                  result.title,
                  style: const TextStyle(
                    color: Colors.blue,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                subtitle: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      result.url,
                      style: const TextStyle(color: Colors.green),
                    ),
                    const SizedBox(height: 4),
                    Text(result.snippet),
                  ],
                ),
                onTap: () async {
                  final uri = Uri.parse(result.url);
                  if (await canLaunchUrl(uri)) {
                    await launchUrl(uri);
                  }
                },
              ),
            );
          },
        );
      }),
    );
  }
}

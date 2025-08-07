import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../controllers/search_controller.dart';
import '../controllers/analysis_controller.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    final searchController = Get.put(AppSearchController());
    final analysisController = Get.put(AnalysisController());
    final TextEditingController textController = TextEditingController();

    return Scaffold(
      appBar: AppBar(
        title: const Text('AI Agents Frontend'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text(
              'Inserisci le keywords per la ricerca:',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),
            TextField(
              controller: textController,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                hintText: 'Inserisci le tue keywords...',
                prefixIcon: Icon(Icons.search),
              ),
              onSubmitted: (value) => searchController.performSearch(value),
            ),
            const SizedBox(height: 30),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                Obx(
                  () => ElevatedButton.icon(
                    onPressed:
                        searchController.isLoading.value
                            ? null
                            : () => searchController.performSearch(
                              textController.text,
                            ),
                    icon:
                        searchController.isLoading.value
                            ? const SizedBox(
                              width: 16,
                              height: 16,
                              child: CircularProgressIndicator(strokeWidth: 2),
                            )
                            : const Icon(Icons.search),
                    label: const Text('Search'),
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 24,
                        vertical: 12,
                      ),
                    ),
                  ),
                ),
                Obx(
                  () => ElevatedButton.icon(
                    onPressed:
                        analysisController.isLoading.value
                            ? null
                            : () => analysisController.performAnalysis(
                              textController.text,
                            ),
                    icon:
                        analysisController.isLoading.value
                            ? const SizedBox(
                              width: 16,
                              height: 16,
                              child: CircularProgressIndicator(strokeWidth: 2),
                            )
                            : const Icon(Icons.analytics),
                    label: const Text('Analyze'),
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 24,
                        vertical: 12,
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

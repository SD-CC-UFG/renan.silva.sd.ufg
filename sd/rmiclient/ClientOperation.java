package com.sd.rmiclient;

import java.net.MalformedURLException;
import java.rmi.Naming;
import java.rmi.NotBoundException;
import java.rmi.RemoteException;
import java.util.ArrayList;
import java.util.*;
import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;
import java.net.ServerSocket;
import javax.swing.JOptionPane;

import com.sd.rmiinterface.RMIInterface;

public class ClientOperation {
	private static RMIInterface look_up;
	

	public static void main(String[] args) throws MalformedURLException, RemoteException, NotBoundException {
		String meuIp = "";
		String tipo = "";
		Map<String, ArrayList<String>> mapaTopicosDoBroker = new HashMap<String, ArrayList<String>>(); 
		
		String tipoUsuario = JOptionPane.showInputDialog("Digite P para Publisher, S para Subscribe ou B para broker ?");

		//Se comunica com o servidor de nomes para fazer o pub/sub
		look_up = (RMIInterface) Naming.lookup("//localhost/MyServer");

		if (tipoUsuario.equals("P")) {
			//É escolhido um broker e retornado para que o cliente se comunique com o broker nao-central
			String brokerIP = look_up.buscarBroker();
			System.err.println("broker selecionado: " + brokerIP);

			String topico = JOptionPane.showInputDialog("Digite um topico");
			
			String texto = JOptionPane.showInputDialog("Digite um texto para o topico");

			//Publicar um topico para os inscritos lerem
			publicarInscreverNoTopico(topico, texto, brokerIP, meuIp);

			System.err.println("Publicacao enviada: " + texto); 
			
		} else if (tipoUsuario.equals("S")) {
			//É escolhido um broker e retornado para que o cliente se comunique com o broker nao-central
			String brokerIP = look_up.buscarBroker();

			meuIp = "127.0.0.1:" + JOptionPane.showInputDialog("Digite seu IP(127.0.0.1:12345):");
			String topico = JOptionPane.showInputDialog("Digite um topico: ");

			System.err.println("Inscrito em: " + topico); 

			publicarInscreverNoTopico(topico, ":STAQ"+meuIp, brokerIP, meuIp);
			mensagemDosTopicosAssinados(meuIp);

		} else if(tipoUsuario.equals("B")) {
			// inscreverBroker
			meuIp = "127.0.0.1:" + JOptionPane.showInputDialog("Digite seu IP(127.0.0.1:12345):");
			tipo = JOptionPane.showInputDialog("Voce e um broker central ou externo? (C/E)");
			System.err.println(look_up.inscreverBroker(meuIp, tipo));

			//Criar thread que fica esperando as publicacoes
			mensagemDosTopicos(mapaTopicosDoBroker, meuIp, tipo);
		}

 	
	}

	public static String publicarInscreverNoTopico(String topico, String texto, String brokerIP, String meuIp) throws RemoteException{
		//Criar thread que envia o topico e texto para o brokerIP
		try {
            Socket socket = new Socket(brokerIP.substring(0, brokerIP.indexOf(":")), Integer.valueOf(brokerIP.substring(brokerIP.indexOf(":")+1, brokerIP.length())));

            DataOutputStream fluxoSaidaDados = new DataOutputStream(socket.getOutputStream());
            threadEnviarTopicoParaBroker(fluxoSaidaDados, texto, topico, meuIp);

        } catch (IOException iec) {
            System.out.println(iec.getMessage());
        }

		return "Publicado";
	}

	private static void threadEnviarTopicoParaBroker(final DataOutputStream fluxoSaidaDados, final String texto, final String topico, final String meuIp) throws IOException {

        new Thread() {
            public void run() {
                try {
                    fluxoSaidaDados.writeUTF(topico + "-" + texto + "[" + meuIp);
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
        }.start();
    }

	private static void mensagemDosTopicos(Map<String, ArrayList<String>> mapaTopicosDoBroker, String meuIp, String tipo) {
        new Thread(){
            public void run(){
                try {

                	ServerSocket servidorSocket = new ServerSocket(Integer.valueOf(meuIp.substring(meuIp.indexOf(":")+1, meuIp.length())));

                    while(true){
						Socket socket = servidorSocket.accept();
                    	DataInputStream fluxoEntradaDados = new DataInputStream(socket.getInputStream());
                        String mensagem = fluxoEntradaDados.readUTF();

                        //Salvar no mapa de topicos o topico
                        ArrayList<String> inscritos = new ArrayList<>();

                        String topico = mensagem.substring(0, mensagem.indexOf("-"));
                        String texto = mensagem.substring(mensagem.indexOf("-")+1, mensagem.indexOf("["));
                        String ultimoIp = mensagem.substring(mensagem.indexOf("[")+1, mensagem.length());

                        //Inscrever no topico
                        if (texto.contains(":") && texto.substring(0, texto.indexOf(":")+5).equals(":STAQ")) {
	                        if (mapaTopicosDoBroker.containsKey(topico)) {
								inscritos = mapaTopicosDoBroker.get(topico);
								inscritos.add(texto.substring(texto.indexOf(":")+5, texto.length()));
								mapaTopicosDoBroker.put(topico, inscritos);
							} else {
								inscritos.add(texto.substring(texto.indexOf(":")+5, texto.length()));
								mapaTopicosDoBroker.put(topico, inscritos);
							}

							System.err.println("Cliente: " + texto.substring(texto.indexOf(":")+5, texto.length()) + " inscrito no topico: " + topico);
						} else {

	                        //Usar algoritmo de filtering para repassar aos outros brokers
	                        ArrayList<String> listaBrokerDoBroker = look_up.listaAdjacencia(meuIp, tipo);
	                        System.err.println("lista de brokers: ");
	                        for (String broker : listaBrokerDoBroker) {
	                        	System.err.println(broker + " - " + ultimoIp);
	                        	if (broker.contains(":") && !broker.equals(ultimoIp)) {
	                        		publicarInscreverNoTopico(topico, texto, broker.substring(broker.indexOf(":"), broker.length()), meuIp);
	                        	}
	                        }
	                        
	                        //Enviar aos inscritos que assinam o topico
	                        // publicar(String topico, String texto, String inscritoIP) para cada inscrito
	                        if (tipo.equals("E")) {
								inscritos = new ArrayList<>();
		                        if (mapaTopicosDoBroker.containsKey(topico)) {
									inscritos = mapaTopicosDoBroker.get(topico);
									System.err.println("topico: " + topico);
									System.err.println("texto:" + texto);
									for (String inscrito : inscritos) {
			                        	publicarInscreverNoTopico(topico, texto, inscrito.substring(inscrito.indexOf(":"), inscrito.length()), meuIp);
			                        }
								}
	                        }
	                        
							System.err.println("topicos: ");
							for (Map.Entry<String, ArrayList<String>> entry : mapaTopicosDoBroker.entrySet()) {
								System.err.println(entry.getKey());
							}
						}
                    }
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
        }.start();
    }

	private static void mensagemDosTopicosAssinados(String meuIp) {
    	new Thread(){
        	public void run(){
            	try {

	            	ServerSocket servidorSocket = new ServerSocket(Integer.valueOf(meuIp.substring(meuIp.indexOf(":")+1, meuIp.length())));

	                while(true){
						Socket socket = servidorSocket.accept();
	                	DataInputStream fluxoEntradaDados = new DataInputStream(socket.getInputStream());
	                    String mensagem = fluxoEntradaDados.readUTF();

						String topico = mensagem.substring(0, mensagem.indexOf("-"));
                        String texto = mensagem.substring(mensagem.indexOf("-")+1, mensagem.indexOf("["));

	                    System.err.println("Topico:" + topico + "\n" + "Texto:" + texto);
                	}
				} catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
        	}
    	}.start();
    }
}

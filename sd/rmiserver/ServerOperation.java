package com.sd.rmiserver;

import java.rmi.Naming;
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.util.ArrayList;
import java.util.*;
import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.DataInputStream;
//import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;

import com.sd.rmiinterface.RMIInterface;

public class ServerOperation extends UnicastRemoteObject implements RMIInterface{
	private static final long serialVersionUID = 1L;
	Map<String, ArrayList<String>> mapaTopicos = new HashMap<String, ArrayList<String>>(); 
	Map<String, Integer> listaBrokersCentrais = new HashMap<String, Integer>(); 
	Map<String, Integer> listaBrokersExternos = new HashMap<String, Integer>(); 
	private ArrayList<String> inscritos = new ArrayList<>();
	Map<String, ArrayList<String>> mapaDeAdjacencia = new HashMap<String, ArrayList<String>>(); 
	Map<String, ArrayList<String>> mapaDeAdjacenciaExterno = new HashMap<String, ArrayList<String>>(); 

	protected ServerOperation() throws RemoteException {
		super();
	}

	//Brokers
	@Override
	public String buscarBroker() throws RemoteException{
		//Busca um broker externo para fazer os pub/sub (busca o broker com o menor numero de conexoes)
		String ipBroker = "";
		Integer valor = Integer.MAX_VALUE;

		for (Map.Entry<String, Integer> entry : listaBrokersExternos.entrySet()) {
		    if (valor > entry.getValue()) {
		    	valor = entry.getValue();
		        ipBroker = entry.getKey();
		    }
		}

		if (ipBroker == "") {
			return "";
		}

		//Atualiza o numero de conexoes desse broker
	    Integer conexoes = listaBrokersExternos.get(ipBroker);

	    listaBrokersExternos.put(ipBroker, conexoes+1);

		return ipBroker;
	}

	public String buscarBrokerCentral() throws RemoteException{
		//Busca um broker externo para fazer os pub/sub (busca o broker com o menor numero de conexoes)
		String ipBroker = "";
		Integer valor = Integer.MAX_VALUE;

		for (Map.Entry<String, Integer> entry : listaBrokersCentrais.entrySet()) {
		    if (valor > entry.getValue()) {
		    	valor = entry.getValue();
		        ipBroker = entry.getKey();
		    }
		}

		if (ipBroker == "") {
			return "";
		}

		//Atualiza o numero de conexoes desse broker
	    Integer conexoes = listaBrokersCentrais.get(ipBroker);

	    listaBrokersCentrais.put(ipBroker, conexoes+1);

		return ipBroker;
	}

	//Colcoar para retornar a lista de brokers ligados a ele
	@Override
	public String inscreverBroker(String ipBroker, String tipo) throws RemoteException{
		//Coloca o broker na lsita de brokers
		if (tipo.equals("C")) {
			//Cria sua chave no mapa de adjacencia
			if (!listaBrokersCentrais.containsKey(ipBroker)) {
				listaBrokersCentrais.put(ipBroker, 0);
				mapaDeAdjacencia.put(ipBroker, new ArrayList<String>());
			}

			//Criar o mapa de adjacencia
			for (Map.Entry<String, ArrayList<String>> entry : mapaDeAdjacencia.entrySet()) {
				if (!entry.getKey().equals(ipBroker)) {
					ArrayList<String> lista = entry.getValue();
					lista.add(ipBroker);
			    	mapaDeAdjacencia.put(entry.getKey(), lista);

			    	ArrayList<String> listapropria = mapaDeAdjacencia.get(ipBroker);
			    	listapropria.add(entry.getKey());
			    	mapaDeAdjacencia.put(ipBroker, listapropria);
				}
			}

		} else if (tipo.equals("E")) {
			if (!listaBrokersExternos.containsKey(ipBroker)) {
				listaBrokersExternos.put(ipBroker, 0);

				String ipBrokerCentralAdjacente = buscarBrokerCentral();
				if (!mapaDeAdjacenciaExterno.containsKey(ipBroker)) {
					//Adiciona no broker central a adjacencia com esse broker externo
					if (mapaDeAdjacencia.containsKey(ipBrokerCentralAdjacente)) {
						ArrayList<String> lista = mapaDeAdjacencia.get(ipBrokerCentralAdjacente);
						lista.add(ipBroker);
						mapaDeAdjacencia.put(ipBroker, lista);
					}
					//Adiciona a adjacencia do broker externo com o broker central
					mapaDeAdjacenciaExterno.put(ipBroker, new ArrayList<String>(Arrays.asList(ipBrokerCentralAdjacente)));
				}
			}
		}

		System.err.println("Brokers Centrais: ");

		for (Map.Entry<String, Integer> entry : listaBrokersCentrais.entrySet()) {
		    System.err.println(entry.getKey() + "-" + entry.getValue());
		}

		System.err.println("Brokers Externos: ");

		for (Map.Entry<String, Integer> entry : listaBrokersExternos.entrySet()) {
		    System.err.println(entry.getKey()+ "-" + entry.getValue());
		}
		
		System.err.println("\n");
		
		return "Broker inscrito!";
	}

	@Override
	public ArrayList<String> listaAdjacencia(String ipBroker, String tipo) throws RemoteException{
		//Pega a lista de adjacencia
		if (tipo.equals("C")) {
			for (Map.Entry<String, ArrayList<String>> entry : mapaDeAdjacencia.entrySet()) {
				if (entry.getKey().equals(ipBroker)) {
			    	return entry.getValue();
				}
			}
		} else {
			for (Map.Entry<String, ArrayList<String>> entry : mapaDeAdjacenciaExterno.entrySet()) {
				if (entry.getKey().equals(ipBroker)) {
			    	return entry.getValue();
				}
			}
		}
		return new ArrayList<String>();
	}
	
	public static void main(String[] args){
		try {
			Naming.rebind("//localhost/MyServer", new ServerOperation());            
            System.err.println("Server ready");
            
        } catch (Exception e) {
        	System.err.println("Server exception: " + e.toString());
          e.printStackTrace();
        }
	}
}
